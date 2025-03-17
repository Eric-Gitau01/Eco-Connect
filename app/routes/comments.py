from flask import Blueprint, request, jsonify
from app.models.comment import Comment
from app import db

comments_bp = Blueprint('comments', __name__)

@comments_bp.route('/', methods=['POST'])
def add_comment():
    data = request.get_json()
    new_comment = Comment(
        user_id=data.get('user_id'),
        issue_id=data.get('issue_id'),
        content=data.get('content')
    )
    db.session.add(new_comment)
    db.session.commit()
    return jsonify({'message': 'Comment added successfully'}), 201

@comments_bp.route('/<int:comment_id>', methods=['GET'])
def get_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    return jsonify({
        'id': comment.id,
        'user_id': comment.user_id,
        'issue_id': comment.issue_id,
        'content': comment.content,
        'created_at': comment.created_at
    })

@comments_bp.route('/<int:comment_id>', methods=['PUT'])
def update_comment(comment_id):
    data = request.get_json()
    comment = Comment.query.get_or_404(comment_id)
    comment.content = data.get('content', comment.content)
    db.session.commit()
    return jsonify({'message': 'Comment updated successfully'})

@comments_bp.route('/<int:comment_id>', methods=['DELETE'])
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    db.session.delete(comment)
    db.session.commit()
    return jsonify({'message': 'Comment deleted successfully'})
