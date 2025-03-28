from flask import Blueprint, request, jsonify
from app.models.issue import Issue
from app.models import db
from flask_jwt_extended import get_jwt_identity, jwt_required


issues_bp = Blueprint('issues', __name__)



# Create a new issue
@issues_bp.route('/', methods=['POST'])
@issues_bp.route('', methods=['POST'])
@jwt_required()
def create_issue():
    user_id = get_jwt_identity()
    data = request.get_json()


    # Ensure data is present
    if not data:
        return jsonify({'error': 'Missing JSON data'}), 400
    
    required_fields = ['title', 'location','description']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({'error': f'Missing fields: {", ".join(missing_fields)}'}), 400
   
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
@issues_bp.route('', methods=['GET'])
def get_issues():
    issues = Issue.query.all()
    issues_list = [{
        'id': issue.id,
        'title': issue.title,
        'location': issue.location,
        'description': issue.description,
        'user_id': issue.user_id,
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
        'location': issue.location,
        'description': issue.description,
        'user_id': issue.user_id,
        'created_at': issue.created_at
    })

# update a new issue
@issues_bp.route('/<int:issue_id>', methods=['PUT', 'DELETE'])
@jwt_required()
def update_issue(issue_id):
    current_user_id = get_jwt_identity()
    issue = Issue.query.get_or_404(issue_id)

    # Ensure user is the owner of the issue
    if issue.user_id != current_user_id:
        return jsonify({'error': 'Unauthorized to modify the issue'}), 403
    
    if request.method == 'PUT':
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Missing JSON data'}), 400
        
        issue.title = data.get('title', issue.title)
        issue.location = data.get('location', issue.location)
        issue.description = data.get('description', issue.description)
        db.session.commit()
        return jsonify({'message': 'Issue updated successfully'})
 
    
    elif request.method == 'DELETE':
        db.session.delete(issue)
        db.session.commit()
        return jsonify({'message': 'Issue deleted successfully'})
    