import io
import json
import uuid

import boto3
from flask import (
    abort,
    current_app,
    redirect,
    render_template,
    request,
    send_file,
    session,
    url_for,
)
from sqlalchemy import func
from werkzeug.exceptions import BadRequest, HTTPException

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
    build_browse_consignment_query,
    build_browse_query,
    build_browse_series_query,
)
from app.main.flask_config_helpers import (
    get_keycloak_instance_from_flask_config,
)
from app.main.util.date_filters_validator import validate_date_filters
from app.main.util.filter_sort_builder import (
    build_browse_consignment_filters,
    build_filters,
    build_sorting_orders,
)
from app.main.util.pagination import (
    calculate_total_pages,
    get_pagination,
    paginate,
)
from app.main.util.render_utils import (
    create_presigned_url,
    generate_breadcrumb_values,
    generate_image_manifest,
    generate_pdf_manifest,
    get_download_filename,
    get_file_details,
    get_file_mimetype,
)
from app.main.util.search_utils import (
    build_search_results_summary_query,
    build_search_transferring_body_query,
    execute_search,
    extract_search_terms,
    get_open_search_fields_to_search_on,
    get_pagination_info,
    get_param,
    get_query_and_search_area,
    post_process_opensearch_results,
    setup_opensearch,
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
    session["user_id"] = decoded_access_token["sub"]
    ayr_user = AYRUser(session.get("user_groups"))
    if ayr_user.is_all_access_user:
        session["user_type"] = "all_access_user"
    else:
        session["user_type"] = "standard_user"

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
        # all access user (all_access_user)
        for body in Body.query.all():
            transferring_bodies.append(body.Name)

        date_validation_errors = []
        from_date = None
        to_date = None
        date_filters = {}
        date_error_fields = []

        if len(request.args) > 0:
            (
                date_validation_errors,
                from_date,
                to_date,
                date_filters,
                date_error_fields,
            ) = validate_date_filters(request.args)

        filters = build_filters(request.args, from_date, to_date)
        sorting_orders = build_sorting_orders(request.args)

        # set default sort
        if len(sorting_orders) == 0:
            sorting_orders["transferring_body"] = "asc"

        query = build_browse_query(
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

        pagination = get_pagination(page, browse_results.pages)

        return render_template(
            "browse.html",
            form=form,
            current_page=page,
            browse_type="browse",
            results=browse_results,
            date_validation_errors=date_validation_errors,
            date_error_fields=date_error_fields,
            transferring_bodies=transferring_bodies,
            pagination=pagination,
            filters=filters,
            date_filters=date_filters,
            sorting_orders=sorting_orders,
            num_records_found=num_records_found,
            query_string_parameters={
                k: v for k, v in request.args.items() if k not in "page"
            },
            id=None,
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
    body = db.session.get(Body, _id)
    validate_body_user_groups_or_404(body.Name)

    breadcrumb_values = {0: {"transferring_body": body.Name}}

    form = SearchForm()
    page = int(request.args.get("page", 1))
    per_page = int(current_app.config["DEFAULT_PAGE_SIZE"])

    date_validation_errors = []
    from_date = None
    to_date = None
    date_filters = {}
    date_error_fields = []

    if len(request.args) > 0:
        (
            date_validation_errors,
            from_date,
            to_date,
            date_filters,
            date_error_fields,
        ) = validate_date_filters(request.args)

    filters = build_filters(request.args, from_date, to_date)
    sorting_orders = build_sorting_orders(request.args)

    # set default sort
    if len(sorting_orders) == 0:
        sorting_orders["series"] = "asc"

    query = build_browse_query(
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

    pagination = get_pagination(page, browse_results.pages)

    return render_template(
        "browse.html",
        form=form,
        current_page=page,
        browse_type="transferring_body",
        results=browse_results,
        date_validation_errors=date_validation_errors,
        date_error_fields=date_error_fields,
        breadcrumb_values=breadcrumb_values,
        pagination=pagination,
        filters=filters,
        date_filters=date_filters,
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
    series = db.session.get(Series, _id)
    body = series.body
    validate_body_user_groups_or_404(body.Name)

    breadcrumb_values = {
        0: {"transferring_body_id": body.BodyId},
        1: {"transferring_body": body.Name},
        2: {"series": series.Name},
    }

    form = SearchForm()
    page = int(request.args.get("page", 1))
    per_page = int(current_app.config["DEFAULT_PAGE_SIZE"])

    date_validation_errors = []
    from_date = None
    to_date = None
    date_filters = {}
    date_error_fields = []

    if len(request.args) > 0:
        (
            date_validation_errors,
            from_date,
            to_date,
            date_filters,
            date_error_fields,
        ) = validate_date_filters(request.args)

    filters = build_filters(request.args, from_date, to_date)
    sorting_orders = build_sorting_orders(request.args)

    # set default sort
    if len(sorting_orders) == 0:
        sorting_orders["last_record_transferred"] = "desc"

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

    pagination = get_pagination(page, browse_results.pages)

    return render_template(
        "browse.html",
        form=form,
        current_page=page,
        browse_type="series",
        results=browse_results,
        date_validation_errors=date_validation_errors,
        date_error_fields=date_error_fields,
        breadcrumb_values=breadcrumb_values,
        pagination=pagination,
        filters=filters,
        date_filters=date_filters,
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
    consignment = db.session.get(Consignment, _id)
    body = consignment.series.body
    validate_body_user_groups_or_404(body.Name)

    series = consignment.series
    breadcrumb_values = {
        0: {"transferring_body_id": body.BodyId},
        1: {"transferring_body": body.Name},
        2: {"series_id": series.SeriesId},
        3: {"series": series.Name},
        4: {"consignment_reference": consignment.ConsignmentReference},
    }

    form = SearchForm()
    page = int(request.args.get("page", 1))
    per_page = int(current_app.config["DEFAULT_PAGE_SIZE"])

    date_validation_errors = []
    from_date = None
    to_date = None
    date_filters = {}
    date_error_fields = []

    if len(request.args) > 0:
        (
            date_validation_errors,
            from_date,
            to_date,
            date_filters,
            date_error_fields,
        ) = validate_date_filters(request.args, browse_consignment=True)

    filters = build_browse_consignment_filters(request.args, from_date, to_date)
    sorting_orders = build_sorting_orders(request.args)

    # set default sort
    if len(sorting_orders) == 0:
        sorting_orders["date_last_modified"] = "desc"

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

    pagination = get_pagination(page, browse_results.pages)

    return render_template(
        "browse.html",
        form=form,
        current_page=page,
        browse_type="consignment",
        results=browse_results,
        date_validation_errors=date_validation_errors,
        date_error_fields=date_error_fields,
        breadcrumb_values=breadcrumb_values,
        pagination=pagination,
        filters=filters,
        date_filters=date_filters,
        sorting_orders=sorting_orders,
        num_records_found=num_records_found,
        query_string_parameters={
            k: v for k, v in request.args.items() if k not in "page"
        },
    )


@bp.route("/search", methods=["GET"])
@access_token_sign_in_required
def search():
    form_data = request.form.to_dict()
    args_data = request.args.to_dict()

    # merge both dictionaries (args takes precedence over form if there are overlapping keys)
    params = {**form_data, **args_data}

    transferring_body_id = params.get("transferring_body_id", "")

    ayr_user = AYRUser(session.get("user_groups"))

    if ayr_user.is_standard_user or transferring_body_id:
        if not transferring_body_id:
            transferring_body_id = str(
                Body.query.filter(Body.Name == ayr_user.transferring_body.Name)
                .first()
                .BodyId
            )
        return redirect(
            url_for(
                "main.search_transferring_body",
                _id=transferring_body_id,
                **params,
            )
        )
    else:
        return redirect(url_for("main.search_results_summary", **params))


@bp.route("/search_results_summary", methods=["GET"])
@access_token_sign_in_required
def search_results_summary():
    ayr_user = AYRUser(session.get("user_groups"))
    if ayr_user.is_standard_user:
        abort(403)

    form = SearchForm()
    per_page = int(current_app.config["DEFAULT_PAGE_SIZE"])
    page = int(request.args.get("page", 1))

    query, search_area = get_query_and_search_area(request)
    filters = {"query": query}
    num_records_found, paginated_results, pagination = 0, [], None

    if query:
        quoted_phrases, single_terms = extract_search_terms(query)
        open_search = setup_opensearch()
        search_fields = get_open_search_fields_to_search_on(search_area)
        sorting_orders = build_sorting_orders(request.args)
        dsl_query = build_search_results_summary_query(
            search_fields, sorting_orders, quoted_phrases, single_terms
        )
        search_results = execute_search(open_search, dsl_query, page, per_page)
        results = search_results["aggregations"][
            "aggregate_by_transferring_body"
        ]["buckets"]

        total_records = 0
        for bucket in results:
            total_records += bucket["doc_count"]

        page_count = calculate_total_pages(len(results), per_page)
        pagination = get_pagination(page, page_count)
        paginated_results = paginate(results, page, per_page)

        if total_records:
            num_records_found = total_records

    return render_template(
        "search-results-summary.html",
        form=form,
        current_page=page,
        filters=filters,
        search_area=search_area,
        results=paginated_results,
        pagination=pagination,
        num_records_found=num_records_found,
        query_string_parameters={
            k: v for k, v in request.args.items() if k not in "page"
        },
        id=None,
    )


@bp.route("/search/transferring_body/<uuid:_id>", methods=["GET"])
@access_token_sign_in_required
def search_transferring_body(_id: uuid.UUID):
    body = db.session.get(Body, _id)
    validate_body_user_groups_or_404(body.Name)

    form = SearchForm()
    per_page = int(current_app.config["DEFAULT_PAGE_SIZE"])
    page = int(request.args.get("page", 1))
    open_all = get_param("open_all", request)
    highlight_tag = f"uuid_prefix_{uuid.uuid4().hex}"

    query, search_area = get_query_and_search_area(request)
    search_filter = (
        request.args.get("search_filter", "").strip()
        if request.args.get("search_filter")
        else None
    )
    filters = {"query": query}

    breadcrumb_values = {
        0: {"query": ""},
        1: {"transferring_body_id": _id},
        2: {"transferring_body": body.Name},
        3: {"search_terms": "‘’"},
    }

    sorting_orders = build_sorting_orders(request.args)
    search_terms, results, pagination, num_records_found = (
        [],
        {"hits": {"total": {"value": 0}, "hits": []}},
        None,
        0,
    )

    if query:
        quoted_phrases, single_terms = extract_search_terms(query)

        if search_filter:
            if search_filter.startswith('"') and search_filter.endswith('"'):
                quoted_phrases.append(search_filter[1:-1])
            else:
                single_terms.append(search_filter.strip())
        search_terms = quoted_phrases + single_terms

        query = f"{query},{search_filter}" if search_filter else query
        filters["query"] = query

        breadcrumb_values[0] = {"query": query}
        display_terms = " + ".join(
            [f"‘{term}’" for term in search_terms if term.strip()]
        )
        breadcrumb_values[3]["search_terms"] = display_terms or query

        open_search = setup_opensearch()
        search_fields = get_open_search_fields_to_search_on(search_area)
        sorting_orders = build_sorting_orders(request.args)
        dsl_query = build_search_transferring_body_query(
            search_fields,
            sorting_orders,
            _id,
            highlight_tag,
            quoted_phrases,
            single_terms,
        )

        search_results = execute_search(open_search, dsl_query, page, per_page)
        results = post_process_opensearch_results(
            search_results["hits"]["hits"]
        )

        total_records, pagination = get_pagination_info(
            search_results, page, per_page
        )
        num_records_found = total_records

    return render_template(
        "search-transferring-body.html",
        form=form,
        current_page=page,
        filters=filters,
        breadcrumb_values=breadcrumb_values,
        results=results,
        num_records_found=num_records_found,
        sorting_orders=sorting_orders,
        search_terms=search_terms,
        search_area=search_area,
        pagination=pagination,
        open_all=open_all,
        highlight_tag=highlight_tag,
        query_string_parameters={
            k: v for k, v in request.args.items() if k != "page"
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
    file = db.session.get(File, record_id)
    ayr_user = AYRUser(session.get("user_groups"))
    can_download_records = ayr_user.can_download_records
    presigned_url = None

    if file is None:
        abort(404)

    validate_body_user_groups_or_404(file.consignment.series.body.Name)

    file_metadata, file_type, file_extension = get_file_details(file)

    breadcrumb_values = generate_breadcrumb_values(file)

    download_filename = get_download_filename(file)

    manifest_url = url_for(
        "main.generate_manifest", record_id=record_id, _external=True
    )

    try:
        presigned_url = create_presigned_url(file)
    except Exception as e:
        current_app.logger.info(
            f"Failed to create presigned url for document render non-javascript fallback {e}"
        )

    return render_template(
        "record.html",
        form=form,
        record=file_metadata,
        breadcrumb_values=breadcrumb_values,
        download_filename=download_filename,
        can_download_records=can_download_records,
        filters={},
        file_type=file_type,
        manifest_url=manifest_url,
        file_extension=file_extension,
        presigned_url=presigned_url,
        supported_render_extensions=current_app.config[
            "SUPPORTED_RENDER_EXTENSIONS"
        ],
    )


@bp.route("/download/<uuid:record_id>")
@access_token_sign_in_required
def download_record(record_id: uuid.UUID):
    file = db.session.get(File, record_id)
    render = request.args.get("render", False)
    ayr_user = AYRUser(session.get("user_groups"))
    can_download_records = ayr_user.can_download_records

    if can_download_records is not True:
        abort(403)

    if file is None:
        abort(404)

    validate_body_user_groups_or_404(file.consignment.series.body.Name)

    s3 = boto3.client("s3")
    bucket = current_app.config["RECORD_BUCKET_NAME"]
    key = f"{file.consignment.ConsignmentReference}/{file.FileId}"

    try:
        s3_file_object = s3.get_object(Bucket=bucket, Key=key)
    except Exception as e:
        current_app.logger.error(f"Failed to get object from S3: {e}")
        abort(404)

    download_filename = file.FileName

    if file.CiteableReference:
        if len(file.FileName.rsplit(".", 1)) > 1:
            download_filename = (
                file.CiteableReference + "." + file.FileName.rsplit(".", 1)[1]
            )

    try:
        file_content = s3_file_object["Body"].read()
        file_type = download_filename.split(".")[-1].lower()
    except Exception as e:
        current_app.logger.error(f"Error reading S3 file content: {e}")
        abort(500)

    content_type = s3_file_object.get("ContentType", "application/octet-stream")

    if render:
        return send_file(
            io.BytesIO(file_content),
            mimetype=get_file_mimetype(file_type),
            as_attachment=False,
            download_name=download_filename,
        )
    else:
        response = send_file(
            io.BytesIO(file_content),
            mimetype=content_type,
            as_attachment=True,
            download_name=download_filename,
        )
    current_app.logger.info(
        json.dumps({"user_id": session["user_id"], "file": key})
    )
    return response


@bp.route("/signed-out", methods=["GET"])
def signed_out():
    return render_template("signed-out.html")


@bp.route("/cookies", methods=["GET"])
def cookies():
    return render_template("cookies.html")


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


@bp.route("/record/<uuid:record_id>/manifest")
@access_token_sign_in_required
def generate_manifest(record_id: uuid.UUID):
    file = db.session.get(File, record_id)

    if file is None:
        abort(404)

    validate_body_user_groups_or_404(file.consignment.series.body.Name)

    s3 = boto3.client("s3")
    bucket = current_app.config["RECORD_BUCKET_NAME"]

    key = f"{file.consignment.ConsignmentReference}/{file.FileId}"

    s3_file_object = s3.get_object(Bucket=bucket, Key=key)

    filename = file.FileName
    file_type = filename.split(".")[-1].lower()

    if file_type == "pdf":
        return generate_pdf_manifest(record_id)
    elif file_type in ["png", "jpg", "jpeg"]:
        return generate_image_manifest(s3_file_object, record_id)
    else:
        return http_exception(BadRequest())
