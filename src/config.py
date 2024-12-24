import os
from datetime import timedelta


class Config:
    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'SQLALCHEMY_DATABASE_URI', 'sqlite:///default.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = os.getenv('SQLALCHEMY_ECHO', 'False').lower() == 'true'

    # General
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret')

    # JWT
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'default_jwt_secret')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        hours=int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 1)))
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(seconds=int(
        os.getenv('JWT_REFRESH_TOKEN_EXPIRES', 86400)))
    JWT_BLACKLIST_ENABLED = os.getenv(
        'JWT_BLACKLIST_ENABLED', 'False').lower() == 'true'
    JWT_BLACKLIST_TOKEN_CHECKS = os.getenv(
        'JWT_BLACKLIST_TOKEN_CHECKS', "access,refresh").split(',')
