from pathlib import Path

from flask import Flask, send_file, send_from_directory


_PKG_DIR = Path(__file__).resolve().parent.parent.parent
_WEB_DIST_DIR = _PKG_DIR / "web" / "dist"
_CONSOLE_INDEX = _WEB_DIST_DIR / "index.html"


def _register_spa_catch_all(app: Flask):
    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def serve_spa(path):
        if not _CONSOLE_INDEX.exists():
            return {"message": "SaRa Web Console is not available."}, 404

        if path and (_WEB_DIST_DIR / path).is_file():
            return send_from_directory(str(_WEB_DIST_DIR), path)

        return send_file(_CONSOLE_INDEX, mimetype="text/html")


def init_blueprints(app: Flask):
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
    _register_spa_catch_all(app)
