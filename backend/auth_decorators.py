import jwt
from functools import wraps
from flask import request, jsonify, current_app, g


def _get_secret():
    return current_app.config.get("JWT_SECRET_KEY") or current_app.config["SECRET_KEY"]


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return jsonify({"error": "Authorization header missing"}), 401

        try:
            token = auth_header.split(" ")[1]

            payload = jwt.decode(
                token,
                _get_secret(),
                algorithms=["HS256"]
            )

            # store current user info for route usage
            g.user_id = payload["sub"]
            g.role = payload["role"]
            g.username = payload["username"]

        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401

        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401

        except Exception:
            return jsonify({"error": "Invalid authorization header"}), 401

        return f(*args, **kwargs)

    return decorated


def admin_required(f):
    @wraps(f)
    @token_required
    def decorated(*args, **kwargs):

        if g.role != "admin":
            return jsonify({"error": "Admin access required"}), 403

        return f(*args, **kwargs)

    return decorated


def company_required(f):
    @wraps(f)
    @token_required
    def decorated(*args, **kwargs):

        if g.role != "company":
            return jsonify({"error": "Company access required"}), 403

        return f(*args, **kwargs)

    return decorated


def student_required(f):
    @wraps(f)
    @token_required
    def decorated(*args, **kwargs):

        if g.role != "student":
            return jsonify({"error": "Student access required"}), 403

        return f(*args, **kwargs)

    return decorated