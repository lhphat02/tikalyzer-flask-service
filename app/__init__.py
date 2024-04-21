from flask import Flask
from flask_cors import CORS
from .api.getUserVideosAnalytics import get_user_videos_analytics_bp

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Register blueprints
    app.register_blueprint(get_user_videos_analytics_bp)

    return app
