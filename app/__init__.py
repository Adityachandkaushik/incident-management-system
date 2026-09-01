from flask import Flask, redirect, url_for, session, render_template
from pathlib import Path

from .models import init_db
from .auth import auth_bp
from .incidents import incidents_bp
from .routes import routes_bp

def create_app():

```
# =====================================================
# PROJECT DIRECTORIES
# =====================================================

base_dir = Path(__file__).resolve().parent.parent

template_dir = base_dir / "templates"
static_dir = base_dir / "static"


# =====================================================
# CREATE FLASK APPLICATION USED FOR BETTER INTERACTION WITH BLUEPRINTS
# =====================================================

app = Flask(
    __name__,
    template_folder=str(template_dir),
    static_folder=str(static_dir)
)


# =====================================================
# APPLICATION CONFIGURATION
# =====================================================

app.config["SECRET_KEY"] = "dev-secret-key"


# =====================================================
# INITIALIZE DATABASE
# =====================================================

init_db()


# =====================================================
# REGISTER BLUEPRINTS
# =====================================================

app.register_blueprint(auth_bp)
app.register_blueprint(incidents_bp)
app.register_blueprint(routes_bp)


# =====================================================
# HOME
# =====================================================

@app.route("/")
def home():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    return redirect(url_for("dashboard"))


# =====================================================
# DASHBOARD
# =====================================================

@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    conn = None

    try:

        from .models import get_db_connection

        conn = get_db_connection()


        # Total incidents

        total_incidents = conn.execute(
            """
            SELECT COUNT(*)
            FROM incidents
            """
        ).fetchone()[0]


        # Open incidents

        open_incidents = conn.execute(
            """
            SELECT COUNT(*)
            FROM incidents
            WHERE status = 'Open'
            """
        ).fetchone()[0]


        # In Progress incidents

        progress_incidents = conn.execute(
            """
            SELECT COUNT(*)
            FROM incidents
            WHERE status = 'In Progress'
            """
        ).fetchone()[0]


        # Resolved incidents

        resolved_incidents = conn.execute(
            """
            SELECT COUNT(*)
            FROM incidents
            WHERE status = 'Resolved'
            """
        ).fetchone()[0]


    except Exception as e:

        print("Dashboard error:", e)

        total_incidents = 0
        open_incidents = 0
        progress_incidents = 0
        resolved_incidents = 0


    finally:

        if conn:
            conn.close()


    return render_template(
        "dashboard.html",

        total_incidents=total_incidents,

        open_incidents=open_incidents,

        progress_incidents=progress_incidents,

        resolved_incidents=resolved_incidents
    )


return app
```
