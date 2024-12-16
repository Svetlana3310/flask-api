from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.config import Config
import logging

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Import models
    from app.models import User, ToDoItem, StoreModel, ItemModel

    # Register blueprints
    from app.routes import auth, main, store, store_items
    app.register_blueprint(auth.auth_bp)
    app.register_blueprint(main.main_bp)
    app.register_blueprint(store.store_bp)
    app.register_blueprint(store_items.item_bp)

    logging.basicConfig(level=logging.INFO)
    app.logger.info("Flask app starting up")

    return app
