from flask import Blueprint, request, jsonify
from app.models.issue import Issue
from app.models import db

issues_bp = Blueprint('issues', __name__)



# Create a new issue
@issues_bp.route('/', methods=['POST'])
def create_issue():
    data = request.get_json()
    new_issue = Issue(
        title=data.get('title'),
        description=data.get('description'),
        user_id=data.get('user_id'),
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