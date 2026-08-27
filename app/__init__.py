from flask import Flask, redirect, url_for, session
from pathlib import Path

from .models import init_db
from .auth import auth_bp
from .incidents import incidents_bp


def create_app():

    # Project root directory
    base_dir = Path(__file__).resolve().parent.parent

    template_dir = base_dir / "templates"
    static_dir = base_dir / "static"

    # Create Flask application
    app = Flask(
        __name__,
        template_folder=str(template_dir),
        static_folder=str(static_dir)
    )

    # Application configuration
    app.config["SECRET_KEY"] = "dev-secret-key"

    # Initialize database
    init_db()

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(incidents_bp)

    # Home route
    @app.route("/")
    def home():

        if "user_id" not in session:
            return redirect(url_for("auth.login"))

        return redirect(url_for("dashboard"))

    # Dashboard route
    @app.route("/dashboard")
    def dashboard():

        if "user_id" not in session:
            return redirect(url_for("auth.login"))

        return f"""
        <h1>Incident Management Dashboard</h1>

        <p>Welcome, {session["user_name"]}</p>

        <p>Role: {session["user_role"]}</p>

        <hr>

        <a href="/incidents/create">
            Create Incident
        </a>

        <br><br>

        <a href="/incidents/">
            View Incidents
        </a>

        <br><br>

        <a href="/logout">
            Logout
        </a>
        """

    return app