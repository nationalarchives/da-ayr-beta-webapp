import io
import os
import json
import uuid

import boto3
from flask import (
    abort,
    current_app,
    jsonify,
    redirect,
    render_template,
    request,
    send_file,
    session,
    url_for,
)
from PIL import Image
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
    build_fuzzy_search_summary_query,
    build_fuzzy_search_transferring_body_query,
    get_file_metadata,
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

from .forms import SearchForm


def get_file_mimetype(file_type):
    if file_type == "pdf":
        return "application/pdf"
    elif file_type in ["png", "jpg", "jpeg"]:
        return f"image/{file_type}"


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

        return render_template(
            "browse.html",
            form=form,
            current_page=page,
            browse_type="browse",
            results=browse_results,
            date_validation_errors=date_validation_errors,
            date_error_fields=date_error_fields,
            transferring_bodies=transferring_bodies,
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

    return render_template(
        "browse.html",
        form=form,
        current_page=page,
        browse_type="transferring_body",
        results=browse_results,
        date_validation_errors=date_validation_errors,
        date_error_fields=date_error_fields,
        breadcrumb_values=breadcrumb_values,
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

    return render_template(
        "browse.html",
        form=form,
        current_page=page,
        browse_type="series",
        results=browse_results,
        date_validation_errors=date_validation_errors,
        date_error_fields=date_error_fields,
        breadcrumb_values=breadcrumb_values,
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

    return render_template(
        "browse.html",
        form=form,
        current_page=page,
        browse_type="consignment",
        results=browse_results,
        date_validation_errors=date_validation_errors,
        date_error_fields=date_error_fields,
        breadcrumb_values=breadcrumb_values,
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
    query = request.form.get("query", "") or request.args.get("query", "")

    transferring_body_id = request.args.get("transferring_body_id", "")

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
                query=query,
            )
        )
    else:
        return redirect(url_for("main.search_results_summary", query=query))


@bp.route("/search_results_summary", methods=["GET"])
@access_token_sign_in_required
def search_results_summary():
    form = SearchForm()
    per_page = int(current_app.config["DEFAULT_PAGE_SIZE"])
    page = int(request.args.get("page", 1))

    query = request.form.get("query", "") or request.args.get("query", "")

    filters = {"query": query.strip()}
    search_results = None
    num_records_found = 0

    if query:
        fuzzy_search_summary_query = build_fuzzy_search_summary_query(query)
        search_results = fuzzy_search_summary_query.paginate(
            page=page, per_page=per_page
        )

        total_records = db.session.query(
            func.sum(fuzzy_search_summary_query.subquery().c.records_held)
        ).scalar()
        if total_records:
            num_records_found = total_records

    return render_template(
        "search-results-summary.html",
        form=form,
        current_page=page,
        filters=filters,
        results=search_results,
        num_records_found=num_records_found,
        query_string_parameters={
            k: v for k, v in request.args.items() if k not in "page"
        },
        id=None,
    )


@bp.route("/search/transferring_body/<uuid:_id>", methods=["GET"])
@access_token_sign_in_required
def search_transferring_body(_id: uuid.UUID):
    form = SearchForm()
    search_results = None
    per_page = int(current_app.config["DEFAULT_PAGE_SIZE"])
    num_records_found = 0
    query = (
        request.form.get("query", "").strip()
        or request.args.get("query", "").strip()
    )

    search_filter = request.args.get("search_filter")
    if search_filter:
        search_filter = search_filter.strip()

    page = int(request.args.get("page", 1))

    filters = {"query": query}
    sorting_orders = build_sorting_orders(request.args)

    breadcrumb_values = {
        0: {"query": ""},
        1: {"transferring_body_id": _id},
        2: {"transferring_body": db.session.get(Body, _id).Name},
    }
    search_terms = []

    if query:
        search_terms = [item for item in query.split(",") if item]
        if search_filter:
            search_terms.append(search_filter)
            query += (
                "," + search_filter if len(search_terms) > 0 else search_filter
            )
            filters = {"query": query}

        breadcrumb_values.update({0: {"query": query}})

        display_terms = ""

        for i in range(len(search_terms)):
            if len(search_terms[i].strip()) > 0:
                display_terms += (
                    "‘"
                    + search_terms[i].strip()
                    + "’"
                    + (" + " if i < len(search_terms) - 1 else "")
                )

        breadcrumb_values.update(
            {3: {"search_terms": query if query == "," else display_terms}}
        )

        fuzzy_search_query = build_fuzzy_search_transferring_body_query(
            query,
            transferring_body_id=_id,
            sorting_orders=sorting_orders,
        )

        search_results = fuzzy_search_query.paginate(
            page=page, per_page=per_page
        )

        total_records = fuzzy_search_query.count()
        if total_records:
            num_records_found = total_records

    return render_template(
        "search-transferring-body.html",
        form=form,
        current_page=page,
        filters=filters,
        breadcrumb_values=breadcrumb_values,
        results=search_results,
        num_records_found=num_records_found,
        sorting_orders=sorting_orders,
        search_terms=search_terms,
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
    file = db.session.get(File, record_id)
    file_type = None

    if file is None:
        abort(404)

    validate_body_user_groups_or_404(file.consignment.series.body.Name)

    file_metadata = get_file_metadata(record_id)

    file_extension = file.FileName.split(".")[-1].lower()
    if file_extension == "pdf":
        file_type = "iiif"
    elif file_extension in ["png", "jpg", "jpeg"]:
        file_type = "iiif"

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

    download_filename = None
    if file.CiteableReference:
        if len(file.FileName.rsplit(".", 1)) > 1:
            download_filename = (
                file.CiteableReference + "." + file.FileName.rsplit(".", 1)[1]
            )

    manifest_url = url_for(
        "main.generate_manifest", record_id=record_id, _external=True
    )


    s3 = boto3.client("s3")
    bucket = current_app.config["RECORD_BUCKET_NAME"]
    key = f"{file.consignment.ConsignmentReference}/{file.FileId}"

    try:
        s3_file_object = s3.get_object(Bucket=bucket, Key=key)
        file_content = s3_file_object["Body"].read()
        if file_extension == "pdf":
            static_file_path = os.path.join(current_app.static_folder, f"{record_id}.pdf")
        if file_extension == "png" or file_extension == "jpg":
            static_file_path = os.path.join(current_app.static_folder, f"{record_id}.png")
        with open(static_file_path, 'wb') as static_file:
            static_file.write(file_content)
        
    except Exception as e:
        current_app.logger.error(f"S3 error: {e}")
        abort(404)

    return render_template(
        "record.html",
        form=form,
        record=file_metadata,
        breadcrumb_values=breadcrumb_values,
        download_filename=download_filename,
        filters={},
        file_type=file_type,
        manifest_url=manifest_url,
        file_extension=file_extension,
    )


@bp.route("/download/<uuid:record_id>")
@access_token_sign_in_required
def download_record(record_id: uuid.UUID):
    file = db.session.get(File, record_id)

    if file is None:
        abort(404)

    validate_body_user_groups_or_404(file.consignment.series.body.Name)

    s3 = boto3.client("s3")
    bucket = current_app.config["RECORD_BUCKET_NAME"]
    key = f"{file.consignment.ConsignmentReference}/{file.FileId}"

    try:
        s3_file_object = s3.get_object(Bucket=bucket, Key=key)
    except Exception as e:
        current_app.logger.error(f"S3 error: {e}")
        abort(404)

    download_filename = file.FileName

    if file.CiteableReference:
        if len(file.FileName.rsplit(".", 1)) > 1:
            download_filename = (
                file.CiteableReference + "." + file.FileName.rsplit(".", 1)[1]
            )

    try:
        file_content = s3_file_object["Body"].read()
    except Exception as e:
        current_app.logger.error(f"Error reading S3 file content: {e}")
        abort(500)

    content_type = s3_file_object.get("ContentType", "application/octet-stream")

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


@bp.route("/generate_manifest/<uuid:record_id>")
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


def generate_pdf_manifest(record_id):
    file = db.session.get(File, record_id)

    if file is None:
        abort(404)

    file_name = file.FileName
    file_url = url_for("main.get_file", record_id=record_id, _external=True)

    manifest = {
        "@context": [
            "http://iiif.io/api/presentation/3/context.json",
        ],
        "id": f"{url_for('main.get_file', record_id=record_id, _external=True)}",
        "type": "Manifest",
        "label": {"none": [file_name]},
        "requiredStatement": {
            "label": {"en": ["File name"]},
            "value": {"en": [file_name]},
        },
        "viewingDirection": "left-to-right",
        "behavior": ["individuals"],
        "description": f"Manifest for {file_name}",
        "items": [
            {
                "id": f"{url_for('main.get_file', record_id=record_id, _external=True)}",
                "type": "Canvas",
                "label": {"en": ["test"]},
                "items": [
                    {
                        "id": f"{url_for('main.get_file', record_id=record_id, _external=True)}",
                        "type": "AnnotationPage",
                        "label": {"en": ["test"]},
                        "items": [
                            {
                                "id": f"{url_for('main.get_file', record_id=record_id, _external=True)}",
                                "type": "Annotation",
                                "motivation": "painting",
                                "label": {"en": ["test"]},
                                "body": {
                                    "id": file_url,
                                    "type": "Text",
                                    "format": "application/pdf",
                                },
                                "target": f"{url_for('main.get_file', record_id=record_id, _external=True)}",
                            }
                        ],
                    }
                ],
            }
        ],
    }

    return jsonify(manifest)


def generate_image_manifest(s3_file_object, record_id):
    file = db.session.get(File, record_id)

    if file is None:
        abort(404)

    filename = file.FileName

    image = Image.open(io.BytesIO(s3_file_object["Body"].read()))
    width, height = image.size

    # Get the file from S3 to read dimensions
    s3 = boto3.client("s3")
    bucket = current_app.config["RECORD_BUCKET_NAME"]
    key = f"{file.consignment.ConsignmentReference}/{file.FileId}"

    s3_response_object = s3.get_object(Bucket=bucket, Key=key)
    file_content = s3_response_object["Body"].read()
    image = Image.open(io.BytesIO(file_content))
    width, height = image.size

    file_url = url_for("main.get_file", record_id=record_id, _external=True)

    manifest = {
        "@context": "http://iiif.io/api/presentation/2/context.json",
        "@id": f"{url_for('main.get_file', record_id=record_id, _external=True)}",
        "@type": "sc:Manifest",
        "label": filename,
        "description": f"Manifest for {filename}",
        "sequences": [
            {
                "@id": f"{url_for('main.get_file', record_id=record_id, _external=True)}",
                "@type": "sc:Sequence",
                "canvases": [{
                    "@id": f"{url_for('main.get_file', record_id=record_id, _external=True)}",
                    "@type": "sc:Canvas",
                    "label": "Image 1",
                    "width": width,
                    "height": height,
                    "images": [
                        {
                            "@id": f"{url_for('main.get_file', record_id=record_id, _external=True)}",
                            "@type": "oa:Annotation",
                            "motivation": "sc:painting",
                            "resource": {
                                "@id": file_url,
                                "type": "dctypes:Image",
                                "format": "image/png",
                                "width": width,
                                "height": height,
                            },
                            "on": f"{url_for('main.get_file', record_id=record_id, _external=True)}",
                        }
                    ],
                }],
            }
        ],
    }

    return jsonify(manifest)


@bp.route("/files/<record_id>")
def get_file(record_id=None):
    file = db.session.get(File, record_id)
    if file is None:
        abort(404)

    filename = file.FileName
    s3 = boto3.client("s3")
    bucket = current_app.config["RECORD_BUCKET_NAME"]
    key = f"{file.consignment.ConsignmentReference}/{file.FileId}"

    print("here")
    file_type = filename.split(".")[-1].lower()
    print(get_file_mimetype(file_type))
    
    try:
        s3_response_object = s3.get_object(Bucket=bucket, Key=key)
        file_content = s3_response_object["Body"].read()
        file_type = filename.split(".")[-1].lower()
        print(get_file_mimetype(file_type))


        return send_file(
            io.BytesIO(file_content),
            download_name=filename,
            mimetype=get_file_mimetype(file_type),
            as_attachment=False,
        )
    except Exception as e:
        print("error", e)
        abort(404)
