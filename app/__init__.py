from flask import Flask, g
from flask_compress import Compress
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman
from govuk_frontend_wtf.main import WTFormsHelpers
from jinja2 import ChoiceLoader, PackageLoader, PrefixLoader

from app.logger_config import setup_logging
from app.main.db.models import db

compress = Compress()
limiter = Limiter(
    get_remote_address, default_limits=["2 per second", "60 per minute"]
)
talisman = Talisman()


def null_to_dash(value):
    if value == "null":
        return "-"
    if value is None:
        return "-"
    return value


def create_app(config_class, database_uri=None):
    app = Flask(__name__, static_url_path="/assets")
    app.config.from_object(config_class())

    force_https = False if app.config["TESTING"] else True

    app.jinja_env.lstrip_blocks = True
    app.jinja_env.trim_blocks = True
    app.jinja_env.filters["null_to_dash"] = null_to_dash
    app.jinja_loader = ChoiceLoader(
        [
            PackageLoader("app"),
            PrefixLoader(
                {
                    "govuk_frontend_jinja": PackageLoader(
                        "govuk_frontend_jinja"
                    ),
                    "govuk_frontend_wtf": PackageLoader("govuk_frontend_wtf"),
                }
            ),
        ]
    )

    # Set content security policy
    csp = {
        "default-src": "'self'",
        "script-src": ["'self'"],
    }

    # setup database uri for testing
    if database_uri:
        app.config["SQLALCHEMY_DATABASE_URI"] = database_uri

    # Initialise app extensions
    setup_logging(app)
    db.init_app(app)
    compress.init_app(app)
    limiter.init_app(app)
    talisman.init_app(app, content_security_policy=csp, force_https=force_https)
    WTFormsHelpers(app)

    # setup database components
    with app.app_context():
        # create db objects for testing else use existing database objects
        if database_uri:
            db.create_all()
        else:
            db.Model.metadata.reflect(bind=db.engine, schema="public")

    # Register blueprints
    from app.main import bp as main_bp

    app.register_blueprint(main_bp)

    @app.context_processor
    def inject_authenticated_view_status():
        """
        This context processor is designed to provide information about the authentication
        status of the current view to the templates.
        It specifically checks if the `access_token_sign_in_required` attribute is set on
        the Flask `g` object, indicating whether the current view requires authentication.

        The `access_token_sign_in_required` attribute is typically set by the
        `access_token_sign_in_required` decorator applied to specific routes. This decorator
        is responsible for enforcing access token sign in requirements and protecting routes
        that require authentication.

        The primary purpose of this context processor is to make the `authenticated_view`
        variable available in templates, allowing template logic to conditionally display
        elements based on whether the current view requires authentication or not.

        Example Usage in a Template:
        ```html
        {% if authenticated_view %}
            <!-- Display elements for authenticated views -->
            <div>
                You are signed in.
            </div>
        {% else %}
            <!-- Display elements for views that do not require authentication -->
            <div>
                Please sign in to access this page.
            </div>
        {% endif %}
        ```

        Note: Ensure that the `access_token_sign_in_required` decorator is appropriately
        applied to routes where authentication is required for accurate behavior of
        this context processor.


        Returns:
            dict: A dictionary containing the `authenticated_view` variable, which is a
                boolean indicating whether the current view requires authentication.
        """
        authenticated_view = getattr(g, "access_token_sign_in_required", False)
        return dict(authenticated_view=authenticated_view)

    @app.after_request
    def add_no_caching_headers(r):
        """
        Add headers to tell browsers not to cache the pages to protected routes
        """
        if g.get("access_token_sign_in_required"):
            r.headers["Cache-Control"] = (
                "public, max-age=0, no-cache, no-store, must-revalidate"
            )
            r.headers["Pragma"] = "no-cache"
            r.headers["Expires"] = "0"
        return r

    return app
