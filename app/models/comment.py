from app.models import db
from datetime import datetime, timezone, timedelta

# class Comment(db.Model):
#     __tablename__ = 'comment'

#     id = db.Column(db.Integer, primary_key=True)
#     content = db.Column(db.Text, nullable=False)
#     issue_id = db.Column(db.Integer, db.ForeignKey('issue.id', ondelete='CASCADE'), nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
#     created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

#     # relationships
#     issue = db.relationship('Issue', back_populates='comments')
#     user = db.relationship('User', backref='comments')
    
#     def to_dict(self):
#         return {
#             "id": self.id,
#             "content": self.content,
#             "issue_id": self.issue_id,
#             "user_id": self.user_id,
#             "created_at": self.created_at.isoformat()
#         }
    
    
#     def __repr__(self):
#         return f"<Comment {self.id} by User {self.user_id} on Issue {self.issue_id}>"