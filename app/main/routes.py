import os

from flask import (
    flash,
    json,
    make_response,
    redirect,
    render_template,
    request,
    session,
)
from flask_wtf.csrf import CSRFError
from keycloak import KeycloakOpenID
from werkzeug.exceptions import HTTPException

from app.main import bp
from app.main.forms import CookiesForm

from .forms import SearchForm

# from app.data.data import consignment_response, consignment_files_response


KEYCLOAK_BASE_URI = os.getenv("KEYCLOAK_BASE_URI")
KEYCLOAK_CLIENT_ID = os.getenv("KEYCLOAK_CLIENT_ID")
KEYCLOAK_REALM_NAME = os.getenv("KEYCLOAK_REALM_NAME")
KEYCLOAK_CLIENT_SECRET = os.getenv("KEYCLOAK_CLIENT_SECRET")

# Configure client
keycloak_openid = KeycloakOpenID(
    server_url=KEYCLOAK_BASE_URI,
    client_id=KEYCLOAK_CLIENT_ID,
    realm_name=KEYCLOAK_REALM_NAME,
    client_secret_key=KEYCLOAK_CLIENT_SECRET,
)


sample_records = [
    {
        "title": "1.2_record1.pdf",
        "description": "⚊",
        "last_modified": "2023-01-15",
        "status": "Open",
        "closure_period_years": "⚊",
    },
    {
        "title": "1.1_record2.doc",
        "description": "⚊",
        "last_modified": "2023-02-20",
        "status": "Closed",
        "closure_period_years": 50,
    },
    {
        "title": "record_3.jpg",
        "description": "⚊",
        "last_modified": "2023-09-23",
        "status": "Closed",
        "closure_period_years": 20,
    },
]


@bp.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@bp.route("/login", methods=["GET"])
def login():
    # Get Code With Oauth Authorization Request
    auth_url = keycloak_openid.auth_url(
        redirect_uri="http://localhost:5000/callback",
        scope="email",
        state="your_state_info",
    )

    return redirect(auth_url)


@bp.route("/callback", methods=["GET"])
def callback():
    code = request.args.get("code")

    access_token_response = keycloak_openid.token(
        grant_type="authorization_code",
        code=code,
        redirect_uri="http://localhost:5000/callback",
    )

    session["access_token_response"] = access_token_response
    session["access_token"] = access_token_response["access_token"]
    session["refresh_token"] = access_token_response["refresh_token"]
    session["token_type"] = access_token_response["token_type"]
    session["token_scope"] = access_token_response["scope"]
    session["session_state"] = access_token_response["session_state"]


@bp.route("/accessibility", methods=["GET"])
def accessibility():
    return render_template("accessibility.html")


@bp.route("/dashboard", methods=["GET"])
def dashboard():
    return render_template("dashboard.html")


@bp.route("/search", methods=["GET"])
def search():
    return render_template("search.html")


@bp.route("/results", methods=["GET"])
def results():
    return render_template("results.html")


@bp.route("/poc-search-view", methods=["POST", "GET"])
def poc_search():
    form = SearchForm()
    results = []
    query = request.form.get("query", "").lower()
    if query:
        search_terms = query.split()
        for term in search_terms:
            results.extend(
                [
                    record
                    for record in sample_records
                    if term in record["title"].lower()
                    or term in record["description"].lower()
                    or term in record["status"].lower()
                ]
            )
    num_records_found = len(results)
    return render_template(
        "poc-search.html",
        form=form,
        results=results,
        num_records_found=num_records_found,
    )


@bp.route("/browse", methods=["GET"])
def browse():
    return render_template("browse.html")


@bp.route("/quick-access", methods=["GET"])
def quick_access():
    return render_template("quick-access.html")


# @bp.route("/record", methods=["GET"])
# def record():
#     return render_template(
#         "record.html",
#         consignment=consignment_response,
#         consignment_files=consignment_files_response,
#     )


@bp.route("/all-departments", methods=["GET"])
def departments():
    return render_template("departments.html")


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


@bp.app_errorhandler(HTTPException)
def http_exception(error):
    return render_template(f"{error.code}.html"), error.code


@bp.app_errorhandler(CSRFError)
def csrf_error(error):
    flash("The form you were submitting has expired. Please try again.")
    return redirect(request.full_path)
