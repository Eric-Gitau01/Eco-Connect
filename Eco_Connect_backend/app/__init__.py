from flask import Flask, jsonify
from flask_cors import CORS

from app.config import get_config
from app.extensions import db, migrate, jwt

def create_app(config_name=None):
    """Application factory pattern for Flask app"""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(get_config(config_name))
    
    # Initialize extensions
    initialize_extensions(app)
    
    # Register blueprints
    register_blueprints(app)
    
    # Configure error handlers
    register_error_handlers(app)
    
    # Enable CORS
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # Add a health check endpoint
    @app.route('/health')
    def health_check():
        return jsonify({"status": "healthy"}), 200
    
    return app

def initialize_extensions(app):
    """Initialize Flask extensions"""
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

def register_blueprints(app):
    """Register Flask blueprints"""
    from app.resources.auth import auth_bp
    from app.resources.issues import issues_bp
    from app.resources.comments import comments_bp
    from app.resources.search import search_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(issues_bp, url_prefix='/api/issues')
    app.register_blueprint(comments_bp, url_prefix='/api/comments')
    app.register_blueprint(search_bp, url_prefix='/api/search')

def register_error_handlers(app):
    """Register error handlers"""
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Not found"}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({"error": "Internal server error"}), 500
    
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"error": "Bad request"}), 400
    
    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({"error": "Unauthorized"}), 401
    
    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({"error": "Forbidden"}), 403