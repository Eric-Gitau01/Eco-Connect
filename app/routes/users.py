from flask import Blueprint, jsonify
from app.models.user import User
from app import db


user_bp = Blueprint('users_bp', __name__)

@user_bp.route('/user/', methods=['GET'])
def get_user():
    user = User.query.all()
    return jsonify([{
        'id': user.id,
        'username': user.username,
        'email': user.email
    } for user in user])
