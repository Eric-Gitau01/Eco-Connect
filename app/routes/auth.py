from flask import Blueprint, request, jsonify, current_app, abort
import jwt
from datetime import datetime, timedelta
from app.models import db
from app.models.user import User
from werkzeug.security import generate_password_hash, check_password_hash
#from flask_jwt_extended import create_access_token, create_refresh_token
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

# # User registration
# @auth_bp.route('/register', methods=['POST'])
# def register():
#     data = request.get_json()
#     username = data.get('username')
#     password = data.get('password')
#     email = data.get('email')

#     if not username or not password:
#         return jsonify({'message': 'Username and password are required'}), 400

#     if User.query.filter_by(username=username).first():
#         return jsonify({'message': 'User already exists'}), 400

#     # Store hashed password in the database
#     hashed_password = generate_password_hash(password)
#     new_user = User(username=username, email=email, password=hashed_password)
#     db.session.add(new_user)
#     db.session.commit()

#     return jsonify({'message': 'User created successfully'}), 201


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
        # access_token = create_access_token(identity=str(user.id))
        # refresh_token = create_refresh_token(identity=str(user.id))
        access_token = jwt.encode(
             {'user_id': user.id, 'exp': datetime.utcnow() + timedelta(hours=1)},
             current_app.config['SECRET_KEY'],
             algorithm='HS256')

        refresh_token = str(uuid.uuid4()) # Generate refresh token
        user.refresh_token = refresh_token # Save refresh token to the database
        db.session.commit() # Commit changes to the database

        return jsonify({
            'access_token': access_token,
            'refresh_token': refresh_token,
            'message': 'Login successful'
        }), 200

    return jsonify({'message': 'Invalid credentials'}), 401


# Refresh access token
@auth_bp.route('/refresh-token', methods=['POST'])
def refresh_token():
    try:
        data = request.get_json()
        if not data or 'refresh_token' not in data:
            print("Refresh token is required")
            return jsonify({'message': 'Refresh token is required'}), 400
        
        refresh_token = data.get('refresh_token')
        print(f"Looking for user with refresh token: {refresh_token}")

        # Find user by refresh token
        user = User.query.all()
        print(f"All users and their refresh tokens: {user}")
        user = User.query.filter_by(refresh_token=refresh_token).first()
        print(f"User found: {user}")

        if not user:
            print("No user found with this refresh token")
            return jsonify({'message': 'Invalid refresh token'}), 401
        
        # Ensure refresh token is not empty or expired
        if not user.refresh_token:
            print("Refresh token is empty or expired")
            return jsonify({'message': 'Invalid refresh token'}), 401
        
        
        # Generate new access token
        access_token = jwt.encode(
            {'user_id': user.id, 'exp': datetime.utcnow() + timedelta(hours=1)},
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        )

        # Generate new refresh token and save it to the database
        new_refresh_token = str(uuid.uuid4())
        user.refresh_token = new_refresh_token
        db.session.commit()

        # return the new token as a response
        print(f"New access token and refresh token generated for user {user.id}")
        return jsonify({'access_token': access_token, 'refresh_token': new_refresh_token}), 200
        
    
    except Exception as e:
        print(f"Error during refresh token: {e}")
        return jsonify({'message': 'An  Internal Server Error occurred'}), 500
    


    # data = request.get_json()
    # refresh_token = data.get('refresh_token')

    # user = User.query.filter_by(refresh_token=refresh_token).first()
    # if not user:
    #     return jsonify({'message': 'Invalid refresh token'}), 401

    # access_token = jwt.encode(
    #     {'user_id': user.id, 'exp': datetime.utcnow() + timedelta(hours=1)},
    #     current_app.config['SECRET_KEY'],
    #     algorithm='HS256'
    # )

    # return jsonify({'access_token': access_token}), 200


# # Request password reset
# @auth_bp.route('/request-password-reset', methods=['POST'])
# def request_password_reset():
#     data = request.get_json()
#     email = data.get('email')

#     user = User.query.filter_by(email=email).first()
#     if not user:
#         return jsonify({'message': 'Email not found'}), 404

#     reset_token = jwt.encode(
#         {'user_id': user.id, 'exp': datetime.utcnow() + timedelta(minutes=15)},
#         current_app.config['SECRET_KEY'],
#         algorithm='HS256'
#     )

#     print(f"Password reset link: http://localhost:5000/api/auth/reset-password/{reset_token}")

#     return jsonify({'message': 'Password reset link sent to your email'})


# # Reset password
# @auth_bp.route('/reset-password/<token>', methods=['POST'])
# def reset_password(token):
#     try:
#         data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
#         user = User.query.get(data['user_id'])

#         if not user:
#             return jsonify({'message': 'Invalid token'}), 401

#         new_password= request.get_json().get('password')
#         user.set_password(new_password)
#         db.session.commit()

#         return jsonify({'message': 'Password has been reset successfully'})

#     except jwt.ExpiredSignatureError:
#         return jsonify({'message': 'Token has expired'}), 401
#     except jwt.InvalidTokenError:
#         return jsonify({'message': 'Invalid token'}), 401

# def test_register_user(self):
#     """Test user registration with password."""
#     response = self.client.post('/api/auth/register', json={
#         'username': 'newuser',
#         'password': 'password123'
#     })
#     data = response.get_json()

#     self.assertEqual(response.status_code, 201)
#     self.assertEqual(data['message'], 'User created successfully')
#     self.assertIsNotNone(User.query.filter_by(username='newuser').first())
