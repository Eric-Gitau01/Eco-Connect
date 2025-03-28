import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'eco@20')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'mysql://eco_admin:eco_pass@localhost/eco_connect')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'eco@20')
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    JWT_TOKEN_LOCATION = ['headers', 'cookies']
    JWT_COOKIE_SECURE = True

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql://eco_admin:eco%4020@localhost/eco_connect_test'

class ProductionConfig(Config):
    DEBUG = False
    JWT_COOKIE_SECURE = True

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
}
