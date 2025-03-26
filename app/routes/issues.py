from flask import Blueprint, request, jsonify
from app.models.issue import Issue
from app.models import db
from flask_jwt_extended import get_jwt_identity, jwt_required

issues_bp = Blueprint('issues', __name__)



# Create a new issue
@issues_bp.route('/', methods=['POST'])
@jwt_required()
def create_issue():
    user_id = get_jwt_identity()
    data = request.get_json()
    new_issue = Issue(
        title=data.get('title'),
        description=data.get('description'),
        user_id=user_id,
        location=data.get('location')
    )
    db.session.add(new_issue)
    db.session.commit()
    return jsonify({
        'message': 'Issue created successfully',
        'Issue': {
            'id': new_issue.id,
            'title': new_issue.title,
            'description': new_issue.description,
            'location': new_issue.location
            }
        }), 201

# Get all issues
@issues_bp.route('/', methods=['GET'])
def get_issues():
    issues = Issue.query.all()
    issues_list = [{
        'id': issue.id,
        'title': issue.title,
        'description': issue.description,
        'user_id': issue.user_id,
        'location': issue.location,
        'created_at': issue.created_at
    } for issue in issues]
    
    return jsonify(issues_list), 200


# Get all issues
@issues_bp.route('/<int:issue_id>', methods=['GET'])
def get_issue(issue_id):
    issue = Issue.query.get_or_404(issue_id)
    return jsonify({
        'id': issue.id,
        'title': issue.title,
        'description': issue.description,
        'user_id': issue.user_id,
        'location': issue.location,
        'created_at': issue.created_at
    })

# update a new issue
@issues_bp.route('/<int:issue_id>', methods=['PUT'])
def update_issue(issue_id):
    data = request.get_json()
    issue = Issue.query.get_or_404(issue_id)
    issue.title = data.get('title', issue.title)
    issue.description = data.get('description', issue.description)
    issue.location = data.get('location', issue.location)
    db.session.commit()
    return jsonify({'message': 'Issue updated successfully'})


# Delete an issue
@issues_bp.route('/<int:issue_id>', methods=['DELETE'])
def delete_issue(issue_id):
    issue = Issue.query.get_or_404(issue_id)
    db.session.delete(issue)
    db.session.commit()
    return jsonify({'message': 'Issue deleted successfully'})