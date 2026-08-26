from flask import Flask, redirect, url_for, session
from pathlib import Path

from .models import init_db
from .auth import auth_bp


def create_app():

    base_dir = Path(__file__).resolve().parent.parent
    template_dir = base_dir / "templates"
    static_dir = base_dir / "static"

    app = Flask(
        __name__,
        template_folder=str(template_dir),
        static_folder=str(static_dir)
    )

    app.config["SECRET_KEY"] = "dev-secret-key"

    init_db()

    app.register_blueprint(auth_bp)

    @app.route("/")
    def home():

        if "user_id" not in session:
            return redirect(url_for("auth.login"))

        return redirect(url_for("dashboard"))

    @app.route("/dashboard")
    def dashboard():

        if "user_id" not in session:
            return redirect(url_for("auth.login"))

        return f"""
        <h1>Incident Management Dashboard</h1>
        <p>Welcome, {session["user_name"]}</p>
        <p>Role: {session["user_role"]}</p>

        <a href="/logout">Logout</a>
        """

    return app