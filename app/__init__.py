from flask import Flask

from .config import Config


def create_app():

    app = Flask(
        __name__,
        template_folder="../templates",
        static_folder="../static"
    )

    app.config.from_object(Config)

    from .auth import auth_bp
    from .incidents import incidents_bp
    from .api import api_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(incidents_bp)
    app.register_blueprint(
        api_bp,
        url_prefix="/api"
    )

    return app