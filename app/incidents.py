from flask import Blueprint, request, redirect, url_for, session, render_template
from .models import get_db_connection

incidents_bp = Blueprint("incidents", __name__, url_prefix="/incidents")


@incidents_bp.route("/create", methods=["GET", "POST"])
def create_incident():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if request.method == "POST":

        title = request.form["title"]
        description = request.form["description"]
        priority = request.form["priority"]
        severity = request.form["severity"]

        conn = get_db_connection()

        conn.execute(
            """
            INSERT INTO incidents
            (title, description, priority, severity, status, created_by)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                title,
                description,
                priority,
                severity,
                "Open",
                session["user_id"]
            )
        )

        conn.commit()
        conn.close()

        return redirect(url_for("incidents.list_incidents"))

    return render_template("create_incident.html")


@incidents_bp.route("/")
def list_incidents():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    conn = get_db_connection()

    incidents = conn.execute(
        """
        SELECT incidents.*, users.name AS creator_name
        FROM incidents
        JOIN users ON incidents.created_by = users.id
        ORDER BY incidents.created_at DESC
        """
    ).fetchall()

    conn.close()

    return render_template(
        "incidents.html",
        incidents=incidents
    )