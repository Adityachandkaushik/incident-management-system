import sqlite3

from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

from .models import get_db


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():

    # Already logged-in users do not need to register again
    if "user_id" in session:
        return redirect(url_for("incidents.dashboard"))

    if request.method == "POST":

        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        # Basic validation
        if not username or not password:
            flash("Username and password are required.", "danger")
            return redirect(url_for("auth.register"))

        # Username validation
        if len(username) < 3:
            flash("Username must be at least 3 characters.", "danger")
            return redirect(url_for("auth.register"))

        # Password validation
        if len(password) < 8:
            flash("Password must be at least 8 characters.", "danger")
            return redirect(url_for("auth.register"))

        conn = get_db()

        try:
            conn.execute(
                """
                INSERT INTO users (username, password, role)
                VALUES (?, ?, ?)
                """,
                (
                    username,
                    generate_password_hash(password),
                    "user"
                )
            )

            conn.commit()

            flash("Registration successful. Please login.", "success")

            return redirect(url_for("auth.login"))

        except sqlite3.IntegrityError:
            flash("Username already exists.", "danger")

        except sqlite3.Error:
            flash("Something went wrong. Please try again.", "danger")

        finally:
            conn.close()

    return render_template("register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    # Already logged-in users go directly to dashboard
    if "user_id" in session:
        return redirect(url_for("incidents.dashboard"))

    if request.method == "POST":

        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not username or not password:
            flash("Username and password are required.", "danger")
            return redirect(url_for("auth.login"))

        conn = get_db()

        try:
            user = conn.execute(
                "SELECT * FROM users WHERE username = ?",
                (username,)
            ).fetchone()

        except sqlite3.Error:
            flash("Something went wrong. Please try again.", "danger")
            return redirect(url_for("auth.login"))

        finally:
            conn.close()

        if user and check_password_hash(user["password"], password):

            # Clear any previous session data
            session.clear()

            # Create authenticated session
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            session["role"] = user["role"]

            return redirect(url_for("incidents.dashboard"))

        flash("Invalid username or password.", "danger")

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():

    session.clear()

    flash("You have been logged out.", "success")

    return redirect(url_for("auth.login"))