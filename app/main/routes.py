import uuid

import boto3
from flask import (
    Response,
    current_app,
    flash,
    json,
    make_response,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask_wtf.csrf import CSRFError
from sqlalchemy import func
from werkzeug.exceptions import HTTPException

from app.main import bp
from app.main.authorize.access_token_sign_in_required import (
    access_token_sign_in_required,
)
from app.main.authorize.ayr_user import AYRUser
from app.main.authorize.permissions_helpers import (
    validate_body_user_groups_or_404,
)
from app.main.db.models import Body, Consignment, File, Series, db
from app.main.db.queries import (
    build_browse_all_query,
    build_browse_consignment_query,
    build_browse_series_query,
    build_browse_transferring_body_query,
    build_fuzzy_search_query,
    get_file_metadata,
)
from app.main.flask_config_helpers import (
    get_keycloak_instance_from_flask_config,
)
from app.main.forms import CookiesForm
from app.main.util.filter_sort_builder import (
    build_browse_consignment_filters,
    build_filters,
    build_sorting_orders,
)

from .forms import SearchForm


@bp.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@bp.route("/sign-out", methods=["GET"])
@access_token_sign_in_required
def sign_out():
    keycloak_openid = get_keycloak_instance_from_flask_config()
    keycloak_openid.logout(session["refresh_token"])
    session.clear()

    return redirect("/signed-out")


@bp.route("/sign-in", methods=["GET"])
def sign_in():
    keycloak_openid = get_keycloak_instance_from_flask_config()
    auth_url = keycloak_openid.auth_url(
        redirect_uri=f"{request.url_root}callback",
        scope="group_mapper_client_scope",
    )

    return redirect(auth_url)


@bp.route("/callback", methods=["GET"])
def callback():
    keycloak_openid = get_keycloak_instance_from_flask_config()
    code = request.args.get("code")
    access_token_response = keycloak_openid.token(
        grant_type="authorization_code",
        code=code,
        redirect_uri=f"{request.url_root}callback",
    )

    session["access_token"] = access_token_response["access_token"]
    session["refresh_token"] = access_token_response["refresh_token"]
    decoded_access_token = keycloak_openid.introspect(session["access_token"])
    session["user_groups"] = decoded_access_token["groups"]

    return redirect(url_for("main.browse"))


@bp.route("/accessibility", methods=["GET"])
def accessibility():
    return render_template("accessibility.html")


@bp.route("/browse", methods=["GET"])
@access_token_sign_in_required
def browse():
    form = SearchForm()
    page = int(request.args.get("page", 1))
    per_page = int(current_app.config["DEFAULT_PAGE_SIZE"])
    transferring_bodies = []

    ayr_user = AYRUser(session.get("user_groups"))
    if ayr_user.is_standard_user:
        return redirect(
            f"/browse/transferring_body/{ayr_user.transferring_body.BodyId}"
        )
    else:
        # all access user (superuser)
        for body in Body.query.all():
            transferring_bodies.append(body.Name)

        filters = build_filters(request.args)
        sorting_orders = build_sorting_orders(request.args)

        query = build_browse_all_query(
            filters=filters,
            sorting_orders=sorting_orders,
        )

        browse_results = query.paginate(page=page, per_page=per_page)

        total_records = db.session.query(
            func.sum(query.subquery().c.records_held)
        ).scalar()
        if total_records:
            num_records_found = total_records
        else:
            num_records_found = 0

        return render_template(
            "browse.html",
            form=form,
            current_page=page,
            browse_type="browse",
            results=browse_results,
            transferring_bodies=transferring_bodies,
            filters=filters,
            sorting_orders=sorting_orders,
            num_records_found=num_records_found,
            query_string_parameters={
                k: v for k, v in request.args.items() if k not in "page"
            },
        )


@bp.route("/browse/transferring_body/<uuid:_id>", methods=["GET"])
@access_token_sign_in_required
def browse_transferring_body(_id: uuid.UUID):
    """
    Render the browse transferring body view page.

    This function retrieves search results for a specific
    record(s) based on the transferring_body 'id' provided
    as list of results on the 'browse-transferring-body.html' template.

    Returns:
        A rendered HTML page with transferring body records.
    """
    form = SearchForm()

    page = int(request.args.get("page", 1))
    per_page = int(current_app.config["DEFAULT_PAGE_SIZE"])

    breadcrumb_values = {0: {"transferring_body": Body.query.get(_id).Name}}
    filters = build_filters(request.args)
    sorting_orders = build_sorting_orders(request.args)

    query = build_browse_transferring_body_query(
        transferring_body_id=_id,
        filters=filters,
        sorting_orders=sorting_orders,
    )

    browse_results = query.paginate(page=page, per_page=per_page)

    total_records = db.session.query(
        func.sum(query.subquery().c.records_held)
    ).scalar()
    if total_records:
        num_records_found = total_records
    else:
        num_records_found = 0

    return render_template(
        "browse.html",
        form=form,
        current_page=page,
        browse_type="transferring_body",
        results=browse_results,
        breadcrumb_values=breadcrumb_values,
        filters=filters,
        sorting_orders=sorting_orders,
        num_records_found=num_records_found,
        query_string_parameters={
            k: v for k, v in request.args.items() if k not in "page"
        },
    )


@bp.route("/browse/series/<uuid:_id>", methods=["GET"])
@access_token_sign_in_required
def browse_series(_id: uuid.UUID):
    """
    Render the browse series view page.

    This function retrieves search results for a specific
    record(s) based on the series 'id' provided
    as list of results on the 'browse-series.html' template.

    Returns:
        A rendered HTML page with series records.
    """
    form = SearchForm()
    page = int(request.args.get("page", 1))
    per_page = int(current_app.config["DEFAULT_PAGE_SIZE"])

    series = Series.query.get(_id)
    body = series.body
    breadcrumb_values = {
        0: {"transferring_body_id": body.BodyId},
        1: {"transferring_body": body.Name},
        2: {"series": series.Name},
    }

    filters = build_filters(request.args)
    sorting_orders = build_sorting_orders(request.args)

    query = build_browse_series_query(
        series_id=_id,
        filters=filters,
        sorting_orders=sorting_orders,
    )

    browse_results = query.paginate(page=page, per_page=per_page)

    total_records = db.session.query(
        func.sum(query.subquery().c.records_held)
    ).scalar()
    if total_records:
        num_records_found = total_records
    else:
        num_records_found = 0

    return render_template(
        "browse.html",
        form=form,
        current_page=page,
        browse_type="series",
        results=browse_results,
        breadcrumb_values=breadcrumb_values,
        filters=filters,
        sorting_orders=sorting_orders,
        num_records_found=num_records_found,
        query_string_parameters={
            k: v for k, v in request.args.items() if k not in "page"
        },
    )


@bp.route("/browse/consignment/<uuid:_id>", methods=["GET"])
@access_token_sign_in_required
def browse_consignment(_id: uuid.UUID):
    """
    Render the browse consignment view page.

    This function retrieves search results for a specific
    record(s) based on the consignment 'id' provided
    as list of results on the 'browse-consignment.html' template.

    Returns:
        A rendered HTML page with consignment records.
    """
    form = SearchForm()
    page = int(request.args.get("page", 1))
    per_page = int(current_app.config["DEFAULT_PAGE_SIZE"])

    consignment = Consignment.query.get(_id)
    body = consignment.series.body
    series = consignment.series
    breadcrumb_values = {
        0: {"transferring_body_id": body.BodyId},
        1: {"transferring_body": body.Name},
        2: {"series_id": series.SeriesId},
        3: {"series": series.Name},
        4: {"consignment_reference": consignment.ConsignmentReference},
    }

    filters = build_browse_consignment_filters(request.args)
    sorting_orders = build_sorting_orders(request.args)

    # set default sort for consignment view
    if len(sorting_orders) == 0:
        sorting_orders["closure_type"] = "asc"

    query = build_browse_consignment_query(
        consignment_id=_id,
        filters=filters,
        sorting_orders=sorting_orders,
    )

    browse_results = query.paginate(page=page, per_page=per_page)

    total_records = query.count()
    if total_records:
        num_records_found = total_records
    else:
        num_records_found = 0

    return render_template(
        "browse.html",
        form=form,
        current_page=page,
        browse_type="consignment",
        results=browse_results,
        breadcrumb_values=breadcrumb_values,
        filters=filters,
        sorting_orders=sorting_orders,
        num_records_found=num_records_found,
        query_string_parameters={
            k: v for k, v in request.args.items() if k not in "page"
        },
    )


@bp.route("/search", methods=["GET"])
@access_token_sign_in_required
def search():
    form = SearchForm()
    search_results = None
    sorting_orders = {}
    per_page = int(current_app.config["DEFAULT_PAGE_SIZE"])
    num_records_found = 0
    query = (
        request.form.get("query", "").lower()
        or request.args.get("query", "").lower()
    )
    page = int(request.args.get("page", 1))
    filters = {"query": query}

    if query:
        fuzzy_search_query = build_fuzzy_search_query(query)
        ayr_user = AYRUser(session.get("user_groups"))
        if ayr_user.is_standard_user:
            fuzzy_search_query = fuzzy_search_query.where(
                Body.Name == ayr_user.transferring_body.Name
            )
        search_results = fuzzy_search_query.paginate(
            page=page, per_page=per_page
        )
        num_records_found = search_results.total

    return render_template(
        "search.html",
        form=form,
        current_page=page,
        filters=filters,
        results=search_results,
        num_records_found=num_records_found,
        sorting_orders=sorting_orders,
        query_string_parameters={
            k: v for k, v in request.args.items() if k not in "page"
        },
    )


@bp.route("/record/<uuid:record_id>", methods=["GET"])
@access_token_sign_in_required
def record(record_id: uuid.UUID):
    """
    Render the record details page.

    This function retrieves search results from the session, looks for a specific
    record based on the 'record_id' provided in the query parameters, and renders
    the record details on the 'record.html' template.

    Returns:
        A rendered HTML page with record details.
    """
    form = SearchForm()
    file = File.query.get_or_404(record_id)

    validate_body_user_groups_or_404(file.consignment.series.body.Name)

    file_metadata = get_file_metadata(record_id)

    file = File.query.get(record_id)
    consignment = file.consignment
    body = consignment.series.body
    series = consignment.series
    breadcrumb_values = {
        0: {"transferring_body_id": body.BodyId},
        1: {"transferring_body": body.Name},
        2: {"series_id": series.SeriesId},
        3: {"series": series.Name},
        4: {"consignment_id": consignment.ConsignmentId},
        5: {"consignment_reference": consignment.ConsignmentReference},
        6: {"file_name": file.FileName},
    }

    return render_template(
        "record.html",
        form=form,
        record=file_metadata,
        breadcrumb_values=breadcrumb_values,
    )


@bp.route("/download/<uuid:record_id>")
@access_token_sign_in_required
def download_record(record_id: uuid.UUID):
    file = File.query.get_or_404(record_id)

    validate_body_user_groups_or_404(file.consignment.series.body.Name)

    s3 = boto3.client("s3")
    bucket = current_app.config["RECORD_BUCKET_NAME"]

    key = f"{file.consignment.ConsignmentReference}/{file.FileId}"

    s3_file_object = s3.get_object(Bucket=bucket, Key=key)

    response = Response(
        s3_file_object["Body"].read(),
        headers={"Content-Disposition": "attachment;filename=" + file.FileName},
    )

    return response


@bp.route("/signed-out", methods=["GET"])
def signed_out():
    return render_template("signed-out.html")


@bp.route("/cookies", methods=["GET", "POST"])
def cookies():
    form = CookiesForm()
    # Default cookies policy to reject all categories of cookie
    cookies_policy = {"functional": "no", "analytics": "no"}

    if form.validate_on_submit():
        # Update cookies policy consent from form data
        cookies_policy["functional"] = form.functional.data
        cookies_policy["analytics"] = form.analytics.data

        # Create flash message confirmation before rendering template
        flash("You’ve set your cookie preferences.", "success")

        # Create the response so we can set the cookie before returning
        response = make_response(render_template("cookies.html", form=form))

        # Set cookies policy for one year
        response.set_cookie(
            "cookies_policy", json.dumps(cookies_policy), max_age=31557600
        )
        return response
    elif request.method == "GET":
        if request.cookies.get("cookies_policy"):
            # Set cookie consent radios to current consent
            cookies_policy = json.loads(request.cookies.get("cookies_policy"))
            form.functional.data = cookies_policy["functional"]
            form.analytics.data = cookies_policy["analytics"]
        else:
            # If conset not previously set, use default "no" policy
            form.functional.data = cookies_policy["functional"]
            form.analytics.data = cookies_policy["analytics"]
    return render_template("cookies.html", form=form)


@bp.route("/privacy", methods=["GET"])
def privacy():
    return render_template("privacy.html")


@bp.route("/how-to-use-this-service", methods=["GET"])
def how_to_use():
    return render_template("how-to-use-this-service.html")


@bp.route("/terms-of-use", methods=["GET"])
def terms_of_use():
    return render_template("terms-of-use.html")


@bp.app_errorhandler(HTTPException)
def http_exception(error):
    return render_template(f"{error.code}.html"), error.code


@bp.app_errorhandler(CSRFError)
def csrf_error(error):
    flash("The form you were submitting has expired. Please try again.")
    return redirect(request.full_path)
