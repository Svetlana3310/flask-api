import os
from datetime import timedelta


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret')
    SQLALCHEMY_ECHO = os.getenv('SQLALCHEMY_ECHO', 'true')

    # JWT configuration
    # Change this to your secret key
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    # JWT Token expiration configurations
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=int(os.getenv(
        'JWT_ACCESS_TOKEN_EXPIRES', 1)))  # Convert to integer before using in timedelta
    # Convert to integer (in seconds) for refresh token expiration
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(seconds=int(
        os.getenv('JWT_REFRESH_TOKEN_EXPIRES', 86400)))
    JWT_BLACKLIST_ENABLED = os.getenv('JWT_BLACKLIST_ENABLED')
    JWT_BLACKLIST_TOKEN_CHECKS = os.getenv(
        'JWT_BLACKLIST_TOKEN_CHECKS', ["access", "refresh"])
