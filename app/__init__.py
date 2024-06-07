from flask import Flask
from flask_cors import CORS
from .api.getUserVideosAnalytics import get_user_videos_analytics_bp
from .api.getPredictViewCount import get_predicted_view_count_bp
from .api.getHashtagAnalytics import get_hashtag_videos_analytics_bp
from .api.getTrendingAnalytics import get_trending_videos_analytics_bp
from .api.getUserVideos import get_user_videos_bp
from .api.getUserInfo import get_user_info_bp
from .api.test import get_test_bp

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Register blueprints
    app.register_blueprint(get_user_videos_analytics_bp)
    app.register_blueprint(get_predicted_view_count_bp)
    app.register_blueprint(get_hashtag_videos_analytics_bp)
    app.register_blueprint(get_trending_videos_analytics_bp)
    app.register_blueprint(get_user_videos_bp)
    app.register_blueprint(get_user_info_bp)
    app.register_blueprint(get_test_bp)

    return app
