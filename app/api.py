from flask import Blueprint, request, jsonify, session
from datetime import datetime

from .models import get_db


api_bp = Blueprint("api", __name__)


@api_bp.route("/incidents", methods=["GET"])
def get_incidents():

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

    conn.close()

    return jsonify([
        dict(incident)
        for incident in incidents
    ])


@api_bp.route("/incidents", methods=["POST"])
def create_incident_api():

    if "user_id" not in session:
        return jsonify({
            "error": "Authentication required"
        }), 401

    data = request.get_json()

    title = data.get("title")
    description = data.get("description")
    priority = data.get("priority", "Medium")

    if not title or not description:

        return jsonify({
            "error": "title and description are required"
        }), 400

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

    return jsonify({
        "message": "Incident created",
        "incident_id": incident_id
    }), 201


@api_bp.route("/incidents/<int:incident_id>", methods=["PUT"])
def update_incident(incident_id):

    if "user_id" not in session:
        return jsonify({
            "error": "Authentication required"
        }), 401

    data = request.get_json()

    conn = get_db()

    incident = conn.execute(
        "SELECT * FROM incidents WHERE id = ?",
        (incident_id,)
    ).fetchone()

    if not incident:
        conn.close()

        return jsonify({
            "error": "Incident not found"
        }), 404

    title = data.get("title", incident["title"])
    description = data.get(
        "description",
        incident["description"]
    )
    priority = data.get(
        "priority",
        incident["priority"]
    )
    status = data.get(
        "status",
        incident["status"]
    )

    conn.execute(
        """
        UPDATE incidents
        SET title = ?,
            description = ?,
            priority = ?,
            status = ?
        WHERE id = ?
        """,
        (
            title,
            description,
            priority,
            status,
            incident_id
        )
    )

    conn.commit()
    conn.close()

    return jsonify({
        "message": "Incident updated",
        "incident_id": incident_id
    })


@api_bp.route("/incidents/<int:incident_id>/assign", methods=["PUT"])
def assign_incident_api(incident_id):

    if "user_id" not in session:
        return jsonify({
            "error": "Authentication required"
        }), 401

    if session.get("role") != "admin":
        return jsonify({
            "error": "Admin access required"
        }), 403

    data = request.get_json()

    assigned_to = data.get("assigned_to")

    if not assigned_to:
        return jsonify({
            "error": "assigned_to is required"
        }), 400

    conn = get_db()

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

    return jsonify({
        "message": "Incident assigned"
    })


@api_bp.route("/incidents/<int:incident_id>/resolve", methods=["PUT"])
def resolve_incident_api(incident_id):

    if "user_id" not in session:
        return jsonify({
            "error": "Authentication required"
        }), 401

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

    return jsonify({
        "message": "Incident resolved"
    })