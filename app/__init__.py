import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import logging

db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    # Explicitly set root folder
    app = Flask(__name__,
                template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'templates'),
                static_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'static'))

    app.config.from_object('config.Config')

    # Logging setup
    if not app.debug:
        logging.basicConfig(level=logging.INFO)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'

    # Create tables on startup
    with app.app_context():
        from app.models import User, MoodEntry, Recommendation
        db.create_all()

        # Initialize default recommendations
        from app.recommendations_utils import RecommendationsManager
        RecommendationsManager.initialize_default_recommendations()

    from app import routes
    app.register_blueprint(routes.bp)

    return app