from app.models import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    refresh_token = db.Column(db.String(500), nullable=True)

    issues = db.relationship('Issue', back_populates='user', cascade='all, delete-orphan')    

    # Hashes password before saving to the database 
    def set_password(self, password):
        self.password = generate_password_hash(password)

    # Verifies the password mashes the hash.
    def check_password(self, password):
        return check_password_hash(self.password, password)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
        }
    def set_refresh_token(self, refresh_token):
        self.refresh_token = refresh_token
        db.session.add(self)
        db.session.commit()


    def __repr__(self):
        return f"<User {self.username}>"
