from datetime import datetime
from app.extensions import db

# Association table for issue tags (many-to-many)
issue_tags = db.Table('issue_tags',
    db.Column('issue_id', db.Integer, db.ForeignKey('issues.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True)
)

class Tag(db.Model):
    """Tag model for categorizing issues"""
    __tablename__ = 'tags'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    
    def __repr__(self):
        return f'<Tag {self.name}>'

class Issue(db.Model):
    """Issue model for environmental issues reported by users"""
    __tablename__ = 'issues'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(128))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    severity = db.Column(db.String(20), default='medium')  # low, medium, high, critical
    status = db.Column(db.String(20), default='open')  # open, in_progress, resolved, closed
    image_urls = db.Column(db.JSON)  # Store multiple image URLs as JSON
    upvotes = db.Column(db.Integer, default=0)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Relationships
    comments = db.relationship('Comment', backref='issue', lazy='dynamic', cascade='all, delete-orphan')
    tags = db.relationship('Tag', secondary=issue_tags, backref=db.backref('issues', lazy='dynamic'))
    
    def to_dict(self):
        """Return dictionary representation of the issue (for API responses)"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'location': self.location,
            'coordinates': {
                'latitude': self.latitude,
                'longitude': self.longitude
            } if self.latitude and self.longitude else None,
            'severity': self.severity,
            'status': self.status,
            'image_urls': self.image_urls,
            'upvotes': self.upvotes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'author': {
                'id': self.author.id,
                'username': self.author.username
            },
            'tags': [tag.name for tag in self.tags],
            'comment_count': self.comments.count()
        }
    
    def __repr__(self):
        return f'<Issue {self.title}>'