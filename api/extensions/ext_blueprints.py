def init_blueprints(app):
    """
    Initialize the web blueprint for the application.

    This function registers the web blueprint with the provided Flask application instance.

    :param app: The Flask application instance to register the web blueprint with.
    """
    from flask_cors import CORS
    from controllers.web import web_bp

    CORS(
        web_bp,
        resources={r"/*": {"origins": '*'}},
        supports_credentials=True,
        allow_headers=["Content-Type", "Authorization", "X-App-Code"],
        methods=["GET", "PUT", "POST", "DELETE", "OPTIONS", "PATCH"],
        expose_headers=["X-Version", "X-Env"],
    )
    app.register_blueprint(web_bp)
