from flask import Flask
from .api.crawl.crawl_user_videos import crawl_user_videos_bp
from .api.crawl.crawl_trending_videos import crawl_trending_videos_bp
from .api.crawl.crawl_hashtag_videos import crawl_hashtag_videos_bp
from .api.crawl.crawl_sound_videos import crawl_sound_videos_bp

def create_app():
    app = Flask(__name__)

    # Register blueprints
    app.register_blueprint(crawl_user_videos_bp)
    app.register_blueprint(crawl_trending_videos_bp)
    app.register_blueprint(crawl_hashtag_videos_bp)
    app.register_blueprint(crawl_sound_videos_bp)

    return app
