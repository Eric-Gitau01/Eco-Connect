from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from app.models import db, init_models
from config import config
import pymysql
import logging
from logging.handlers import RotatingFileHandler
import os


# Ensure MySQL compatibility
pymysql.install_as_MySQLdb()

# Initialize extensions
migrate = Migrate()


def create_app(config_name):
    """Factory function to create and configure the Flask app."""
    app = Flask(__name__, static_folder='static')
    app.config.from_object(config[config_name])

    # Initialize JWT manager
    jwt = JWTManager(app)

    # Enable CORS for handling cross-origin requests
    CORS(app)

    # Initialize database and migration tools
    db.init_app(app)
    migrate.init_app(app, db)

    # Import models to ensure they are known by SQLAlchemy
    from app.models import init_models
    with app.app_context():
        init_models()

    # Import and register blueprints (routes)
    from app.routes.auth import auth_bp
    from app.routes.issues import issues_bp
    # from app.routes.comments import comments_bp
    from app.routes.search import search_bp
    from app.routes.home import home_bp
    
#from app.routes.users import users_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(issues_bp, url_prefix='/api/issues')
    #app.register_blueprint(comments_bp, url_prefix='/api/comments')
    app.register_blueprint(search_bp, url_prefix='/api/search')
    app.register_blueprint(home_bp)
#app.register_blueprint(users_bp, url_prefix='/api/users')
    # app.register_blueprint(protected_bp, url_prefix='/api')

    #  set up logging
    if not os.path.exists('logs'):
        os.mkdir('logs')

    file_handler = RotatingFileHandler('logs/error.log', maxBytes=10240, backupCount=10)
    file_handler.setLevel(logging.ERROR)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))

    # Console handler for immediate feedback
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    
    # add handlers to app logger
    app.logger.addHandler(file_handler)
    app.logger.addHandler(console_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Eco-Connect startup')

    # list all registered routes
    with app.app_context():
        print("Registered routes:")
        for rule in app.url_map.iter_rules():
            methods = ', '.join(rule.methods)
            print(f"{rule.endpoint}: {rule.rule} [{methods}]")

    
    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        app.logger.error(f"404 Error: {request.url}")
        return jsonify({"error": "Not Found", "message": "The requested resource was not found."}), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        app.logger.critical(f"500 Internal Server Error at {request.url} - Error: {str(error)}")
        return jsonify({"error": "Internal Server Error", "message": "Something went wrong on our end."}), 500

    @app.errorhandler(400)
    def bad_request_error(error):
        app.logger.warning(f"400 Bad Request: {request.url} - Error: {str(error)}")
        return jsonify({"error": "Bad Request", "message": "The request could not be understood or was missing required parameters."}), 400

    @app.errorhandler(401)
    def unauthorized_error(error):
        app.logger.warning(f"401 Unauthorized Access: {request.url}")
        return jsonify({"error": "Unauthorized", "message": "Authentication is required to access this resource."}), 401

    return app
