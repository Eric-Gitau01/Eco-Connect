from flask import Blueprint, request, jsonify, current_app
import jwt
from datetime import datetime, timezone
from app.models import db
from app.models.user import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    create_access_token, 
    create_refresh_token, 
    jwt_required, 
    get_jwt_identity,
    get_jwt,
    set_access_cookies,
    unset_access_cookies,
    set_refresh_cookies,
    unset_refresh_cookies
)
import uuid


auth_bp = Blueprint('auth', __name__)

# User registration
@auth_bp.route('/register', methods=['POST'])
def register():
    # Get JSON data from request
    data = request.get_json()

    # Extract fields
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')  # Expect plain text password, not hashed

    # Validate required fields
    if not username or not email or not password:
        return jsonify({'message': 'Username, email, and password are required'}), 400

    # Check if username or email already exists
    existing_user = User.query.filter(
        (User.username == username) | (User.email == email)).first()
    if existing_user:
        return jsonify({'message': 'User already exists'}), 409
    
    # Hash password
    hashed_password = generate_password_hash(password)

    # Create and store new user
    new_user = User(username=username, email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User created successfully'}), 201


# User login
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400

    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        # create access and refresh tokens
        access_token = create_access_token(identity=str(user.id))
        refresh_token = create_refresh_token(identity=str(user.id))

        return jsonify({
            'access_token': access_token,
            'refresh_token': refresh_token,
            'message': 'Login successful'
        }), 200

    return jsonify({'message': 'Invalid credentials'}), 401



@auth_bp.route('/logout', methods=['POST'])
@jwt_required(refresh=True) # Require a refresh token to access this route
def logout():
    try:
        user_id = get_jwt_identity()
        current_refresh_token = get_jwt()["jti"]
        current_app.config['JWT_BLACKLIST'].add(current_refresh_token)
        return jsonify({'message': 'Successfully logged out'}), 200
    except Exception as e:
        return jsonify({'error': 'Internal Server Error', 'message': str(e)}), 500


# Refresh access token
@auth_bp.route('/refresh-token', methods=['POST'])
def refresh_token():
    # Get the currents user's identitym from the refresh token
    current_user_id = get_jwt_identity()

    # Create a new access token
    access_token = create_access_token(identity=curent_user_id)

    return jsonify({'access_token': access_token}), 200
