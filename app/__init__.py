from flask import Flask
from flask_cors import CORS   # 👈 ADD THIS
from app.routes.ai_routes import ai_bp

def create_app():
    app = Flask(__name__)

    CORS(app)   # 👈 ADD THIS (IMPORTANT)

    app.register_blueprint(ai_bp)

    return app