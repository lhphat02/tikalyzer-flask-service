from flask import Flask
from .api.getUserVideosAnalytics import get_user_videos_analytics_bp

def create_app():
    app = Flask(__name__)

    # Register blueprints
    app.register_blueprint(get_user_videos_analytics_bp)

    return app
