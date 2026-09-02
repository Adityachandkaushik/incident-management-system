from datetime import datetime

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash
)

from .models import get_db
from .notifications import send_email


incidents_bp = Blueprint("incidents", __name__)


def login_required():
    return "user_id" in session


@incidents_bp.route("/")
def home():

    if "user_id" in session:
        return redirect(url_for("incidents.dashboard"))

    return redirect(url_for("auth.login"))


@incidents_bp.route("/dashboard")
def dashboard():

    if not login_required():
        return redirect(url_for("auth.login"))

    conn = get_db()

    incidents = conn.execute("""
        SELECT
            incidents.*,
            creator.username AS creator_name,
            assignee.username AS assignee_name
        FROM incidents
        LEFT JOIN users creator
            ON incidents.created_by = creator.id
        LEFT JOIN users assignee
            ON incidents.assigned_to = assignee.id
        ORDER BY incidents.id DESC
    """).fetchall()

    users = conn.execute(
        "SELECT id, username FROM users"
    ).fetchall()

    conn.close()

    return render_template(
        "dashboard.html",
        incidents=incidents,
        users=users
    )


@incidents_bp.route("/incident/create", methods=["GET", "POST"])
def create_incident():

    if not login_required():
        return redirect(url_for("auth.login"))

    if request.method == "POST":

        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        priority = request.form.get("priority", "Medium")

        if not title or not description:
            flash(
                "Title and description are required.",
                "danger"
            )
            return redirect(
                url_for("incidents.create_incident")
            )

        conn = get_db()

        cursor = conn.execute(
            """
            INSERT INTO incidents
            (title, description, priority, status, created_by)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                title,
                description,
                priority,
                "Open",
                session["user_id"]
            )
        )

        incident_id = cursor.lastrowid

        conn.commit()
        conn.close()

        flash(
            f"Incident #{incident_id} created successfully.",
            "success"
        )

        return redirect(
            url_for("incidents.dashboard")
        )

    return render_template(
        "create_incident.html"
    )


@incidents_bp.route("/incident/<int:incident_id>")
def incident_detail(incident_id):

    if not login_required():
        return redirect(url_for("auth.login"))

    conn = get_db()

    incident = conn.execute("""
        SELECT
            incidents.*,
            creator.username AS creator_name,
            assignee.username AS assignee_name
        FROM incidents
        LEFT JOIN users creator
            ON incidents.created_by = creator.id
        LEFT JOIN users assignee
            ON incidents.assigned_to = assignee.id
        WHERE incidents.id = ?
    """, (incident_id,)).fetchone()

    # Get users for the assignment dropdown
    users = conn.execute(
        "SELECT id, username FROM users"
    ).fetchall()

    conn.close()

    if not incident:
        flash(
            "Incident not found.",
            "danger"
        )

        return redirect(
            url_for("incidents.dashboard")
        )

    return render_template(
        "incident_detail.html",
        incident=incident,
        users=users
    )


@incidents_bp.route(
    "/incident/<int:incident_id>/assign",
    methods=["POST"]
)
def assign_incident(incident_id):

    if not login_required():
        return redirect(url_for("auth.login"))

    if session.get("role") != "admin":
        flash(
            "Only admin can assign incidents.",
            "danger"
        )

        return redirect(
            url_for("incidents.dashboard")
        )

    assigned_to = request.form.get(
        "assigned_to"
    )

    conn = get_db()

    user = conn.execute(
        "SELECT username FROM users WHERE id = ?",
        (assigned_to,)
    ).fetchone()

    if not user:
        conn.close()

        flash(
            "Invalid user.",
            "danger"
        )

        return redirect(
            url_for("incidents.dashboard")
        )

    conn.execute(
        """
        UPDATE incidents
        SET assigned_to = ?,
            status = 'Assigned'
        WHERE id = ?
        """,
        (
            assigned_to,
            incident_id
        )
    )

    conn.commit()
    conn.close()

    flash(
        f"Incident #{incident_id} assigned to "
        f"{user['username']}.",
        "success"
    )

    return redirect(
        url_for("incidents.dashboard")
    )


@incidents_bp.route(
    "/incident/<int:incident_id>/resolve",
    methods=["POST"]
)
def resolve_incident(incident_id):

    if not login_required():
        return redirect(url_for("auth.login"))

    conn = get_db()

    conn.execute(
        """
        UPDATE incidents
        SET status = 'Resolved',
            resolved_at = ?
        WHERE id = ?
        """,
        (
            datetime.now().isoformat(),
            incident_id
        )
    )

    conn.commit()
    conn.close()

    flash(
        f"Incident #{incident_id} resolved.",
        "success"
    )

    return redirect(
        url_for("incidents.dashboard")
    )