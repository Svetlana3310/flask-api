from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from src.config import Config
import logging

db = SQLAlchemy()
migrate = Migrate()
blacklist = set()
jwt = JWTManager()


@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return (
        jsonify({"message": "The token has expired.", "error": "token_expired"}),
        401,
    )


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return (
        jsonify(
            {"message": "Signature verification failed.", "error": "invalid_token"}
        ),
        401,
    )


@jwt.unauthorized_loader
def missing_token_callback(error):
    return (
        jsonify(
            {
                "description": "Request does not contain an access token.",
                "error": "authorization_required",
            }
        ),
        401,
    )


@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]  # jti = "JWT ID" (unique token identifier)
    return jti in blacklist


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db, directory="src/migrations")
    jwt.init_app(app)

    # Import models
    from src.models import User, ToDoItem, StoreModel, ItemModel

    # Register blueprints
    from src.routes import auth, main, store, store_items
    app.register_blueprint(auth.auth_bp)
    app.register_blueprint(main.main_bp)
    app.register_blueprint(store.store_bp)
    app.register_blueprint(store_items.item_bp)

    logging.basicConfig(level=logging.INFO)
    app.logger.info("Flask app starting up")

    return app
