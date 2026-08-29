from flask import Blueprint, request, redirect, url_for, session, render_template
from .models import get_db_connection


incidents_bp = Blueprint(
    "incidents",
    __name__,
    url_prefix="/incidents"
)


# =========================================================
# CREATE INCIDENT
# =========================================================

@incidents_bp.route("/create", methods=["GET", "POST"])
def create_incident():

    # User must be logged in
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    # GET request → show form
    if request.method == "GET":
        return render_template("create_incident.html")

    # POST request → create incident
    title = request.form.get("title", "").strip()
    description = request.form.get("description", "").strip()
    priority = request.form.get("priority", "Medium")
    severity = request.form.get("severity", "Medium")

    # Validation
    if not title:
        return "Incident title is required.", 400

    if not description:
        return "Incident description is required.", 400

    allowed_priorities = [
        "Low",
        "Medium",
        "High",
        "Critical"
    ]

    allowed_severities = [
        "Low",
        "Medium",
        "High",
        "Critical"
    ]

    if priority not in allowed_priorities:
        return "Invalid priority.", 400

    if severity not in allowed_severities:
        return "Invalid severity.", 400

    # Database connection
    conn = get_db_connection()

    try:

        conn.execute(
            """
            INSERT INTO incidents
            (
                title,
                description,
                priority,
                severity,
                status,
                created_by
            )
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

        print("✅ Incident created successfully")

    except Exception as e:

        conn.rollback()

        print("❌ Error creating incident:", e)

        return f"Database error: {e}", 500

    finally:

        conn.close()

    return redirect(url_for("incidents.list_incidents"))


# =========================================================
# LIST INCIDENTS
# =========================================================

@incidents_bp.route("/")
def list_incidents():

    # User must be logged in
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    conn = get_db_connection()

    try:

        incidents = conn.execute(
            """
            SELECT
                incidents.*,
                users.name AS creator_name
            FROM incidents
            JOIN users
                ON incidents.created_by = users.id
            ORDER BY incidents.created_at DESC
            """
        ).fetchall()

        # Debug output
        print(
            "📋 INCIDENTS:",
            [dict(row) for row in incidents]
        )

    except Exception as e:

        print("❌ Error fetching incidents:", e)

        return f"Database error: {e}", 500

    finally:

        conn.close()

    return render_template(
        "incidents.html",
        incidents=incidents
    )


# =========================================================
# INCIDENT DETAILS
# =========================================================

@incidents_bp.route("/<int:incident_id>")
def incident_detail(incident_id):

    # User must be logged in
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    conn = get_db_connection()

    try:

        incident = conn.execute(
            """
            SELECT
                incidents.*,

                creator.name AS creator_name,
                creator.email AS creator_email,

                engineer.name AS engineer_name

            FROM incidents

            JOIN users AS creator
                ON incidents.created_by = creator.id

            LEFT JOIN users AS engineer
                ON incidents.assigned_to = engineer.id

            WHERE incidents.id = ?
            """,
            (incident_id,)
        ).fetchone()

    except Exception as e:

        print("❌ Error fetching incident:", e)

        return f"Database error: {e}", 500

    finally:

        conn.close()

    # Incident doesn't exist
    if incident is None:
        return "Incident not found.", 404

    return render_template(
        "incident_detail.html",
        incident=incident
    )


# =========================================================
# UPDATE INCIDENT STATUS
# =========================================================

@incidents_bp.route(
    "/<int:incident_id>/status",
    methods=["POST"]
)
def update_status(incident_id):

    # User must be logged in
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    status = request.form.get("status")

    allowed_statuses = [
        "Open",
        "Assigned",
        "In Progress",
        "Resolved",
        "Closed"
    ]

    if status not in allowed_statuses:
        return "Invalid status.", 400

    conn = get_db_connection()

    try:

        conn.execute(
            """
            UPDATE incidents
            SET
                status = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (
                status,
                incident_id
            )
        )

        conn.commit()

        print(
            f"✅ Incident {incident_id} status updated to {status}"
        )

    except Exception as e:

        conn.rollback()

        print("❌ Error updating status:", e)

        return f"Database error: {e}", 500

    finally:

        conn.close()

    return redirect(
        url_for(
            "incidents.incident_detail",
            incident_id=incident_id
        )
    )