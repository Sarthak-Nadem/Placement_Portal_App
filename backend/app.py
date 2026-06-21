from flask import Flask
from flask_cors import CORS

from db import init_db

# Blueprints
from routes.auth_routes import auth_bp
from routes.admin_routes import admin_bp
from routes.company_routes import company_bp
from routes.student_routes import student_bp


app = Flask(__name__)

# Configuration
app.config["SECRET_KEY"] = "your_secret_key"

# CORS
CORS(app)

# Initialize db 
init_db()

# Register Blueprints
app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(admin_bp, url_prefix="/api/admin")
app.register_blueprint(company_bp, url_prefix="/api/company")
app.register_blueprint(student_bp, url_prefix="/api/student")


@app.route("/")
def home():
    return {
        "message": "Placement Portal API Running"
    }


if __name__ == "__main__":
    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )