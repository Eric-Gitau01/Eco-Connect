from app.models import db
from datetime import datetime

class Issue(db.Model):
    __tablename__ = 'issue'

    # Columns
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    user = db.relationship('User', back_populates='issues')
    comments = db.relationship('Comment', back_populates='issue', cascade='all, delete-orphan')

    # Methods
    def __init__(self, title, description, location, user_id):
        self.title = title
        self.description = description
        self.location = location
        self.user_id = user_id

    def to_dict(self):
        """Converts Issue object to a dictionary."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "location": self.location,
            "user_id": self.user_id,
            "created_at": self.created_at.isoformat(),
            "comments": [comment.to_dict() for comment in self.comments] if self.comments else []
        }

    def __repr__(self):
        return f"<Issue {self.id} - {self.title} (User {self.user_id})>"
