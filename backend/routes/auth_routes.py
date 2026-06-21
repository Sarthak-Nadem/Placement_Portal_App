from datetime import datetime, timedelta, timezone

import jwt
from flask import Blueprint, jsonify, request, current_app
from werkzeug.security import check_password_hash, generate_password_hash

from db import get_db

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


def _get_jwt_secret():
    return current_app.config.get("JWT_SECRET_KEY") or current_app.config["SECRET_KEY"]


def _create_access_token(user):
    payload = {
        "sub": user["id"],
        "role": user["role"],
        "username": user["username"],
        "exp": datetime.now(timezone.utc) + timedelta(hours=12),
        "iat": datetime.now(timezone.utc),
    }
    return jwt.encode(payload, _get_jwt_secret(), algorithm="HS256")


def _email_exists(db, email):
    row = db.execute(
        "SELECT id FROM users WHERE email = ?",
        (email,),
    ).fetchone()
    return row is not None


@auth_bp.route("/register/student", methods=["POST"])
def register_student():
    data = request.get_json(silent=True) or {}

    username = (data.get("username") or "").strip()
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    full_name = (data.get("full_name") or username).strip()
    branch = data.get("branch")
    cgpa = data.get("cgpa")
    graduation_year = data.get("graduation_year")
    phone = data.get("phone")

    if not username or not email or not password:
        return jsonify({"error": "username, email and password are required"}), 400

    db = get_db()
    try:
        if _email_exists(db, email):
            return jsonify({"error": "Email already exists"}), 409

        password_hash = generate_password_hash(password)

        user_cursor = db.execute(
            """
            INSERT INTO users (username, email, password, role, active)
            VALUES (?, ?, ?, ?, ?)
            """,
            (username, email, password_hash, "student", 1),
        )

        user_id = user_cursor.lastrowid

        db.execute(
            """
            INSERT INTO students (
                user_id, full_name, branch, cgpa, graduation_year, phone, resume_path
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (user_id, full_name, branch, cgpa, graduation_year, phone, None),
        )

        db.commit()

        return jsonify({
            "message": "Student registered successfully",
        }), 201

    except Exception as e:
        db.rollback()
        return jsonify({"error": f"Student registration failed: {str(e)}"}), 500


@auth_bp.route("/register/company", methods=["POST"])
def register_company():
    data = request.get_json(silent=True) or {}

    username = (data.get("username") or "").strip()
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    company_name = (data.get("company_name") or username).strip()
    hr_name = data.get("hr_name")
    hr_email = (data.get("hr_email") or email).strip().lower()
    website = data.get("website")
    description = data.get("description")

    if not username or not email or not password:
        return jsonify({"error": "username, email and password are required"}), 400

    db = get_db()
    try:
        if _email_exists(db, email):
            return jsonify({"error": "Email already exists"}), 409

        password_hash = generate_password_hash(password)

        user_cursor = db.execute(
            """
            INSERT INTO users (username, email, password, role, active)
            VALUES (?, ?, ?, ?, ?)
            """,
            (username, email, password_hash, "company", 1),
        )

        user_id = user_cursor.lastrowid

        db.execute(
            """
            INSERT INTO companies (
                user_id, company_name, hr_name, hr_email, website,
                description, approval_status, active
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (user_id, company_name, hr_name, hr_email, website, description, "pending", 1),
        )

        db.commit()

        return jsonify({
            "message": "Company registered successfully. Awaiting admin approval."
        }), 201

    except Exception as e:
        db.rollback()
        return jsonify({"error": f"Company registration failed: {str(e)}"}), 500


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}

    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if not email or not password:
        return jsonify({"error": "email and password are required"}), 400

    db = get_db()
    try:
        user = db.execute(
            """
            SELECT id, username, email, password, role, active
            FROM users
            WHERE email = ?
            """,
            (email,),
        ).fetchone()

        if not user:
            return jsonify({"error": "Invalid credentials"}), 401

        if int(user["active"]) == 0:
            return jsonify({"error": "Account is deactivated"}), 403

        if not check_password_hash(user["password"], password):
            return jsonify({"error": "Invalid credentials"}), 401

        if user["role"] == "company":
            company = db.execute(
                """
                SELECT approval_status, active
                FROM companies
                WHERE user_id = ?
                """,
                (user["id"],),
            ).fetchone()

            if not company:
                return jsonify({"error": "Company profile not found"}), 403

            if int(company["active"]) == 0:
                return jsonify({"error": "Company account is deactivated"}), 403

            if company["approval_status"] != "approved":
                return jsonify({"error": "Company account awaiting admin approval"}), 403

        token = _create_access_token(user)

        return jsonify({
            "message": "Login successful",
            "access_token": token,
            "user": {
                "id": user["id"],
                "username": user["username"],
                "email": user["email"],
                "role": user["role"],
            }
        }), 200

    except Exception as e:
        return jsonify({"error": f"Login failed: {str(e)}"}), 500


@auth_bp.route("/logout", methods=["POST"])
def logout():
    return jsonify({
        "message": "Logged out successfully"
    }), 200