from datetime import datetime
from app.extensions import db

class Comment(db.Model):
    """Comment model for user comments on issues"""
    __tablename__ = 'comments'
    
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    upvotes = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    issue_id = db.Column(db.Integer, db.ForeignKey('issues.id'), nullable=False)
    
    # Optional parent comment for nested replies
    parent_id = db.Column(db.Integer, db.ForeignKey('comments.id'), nullable=True)
    replies = db.relationship(
        'Comment',
        backref=db.backref('parent', remote_side=[id]),
        lazy='dynamic',
        cascade='all, delete-orphan'
    )
    
    def to_dict(self, include_replies=False):
        """Return dictionary representation of the comment (for API responses)"""
        result = {
            'id': self.id,
            'content': self.content,
            'upvotes': self.upvotes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'author': {
                'id': self.author.id,
                'username': self.author.username
            },
            'issue_id': self.issue_id,
            'parent_id': self.parent_id
        }
        
        if include_replies and not self.parent_id:  # Only include replies for top-level comments
            result['replies'] = [reply.to_dict() for reply in self.replies]
            
        return result
    
    def __repr__(self):
        return f'<Comment {self.id}>'