from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

# This function will be called during app creation
def init_models():
    from app.models.user import User
    from app.models.issue import Issue
    # from app.models.comment import Comment
    
    # Make these models available at the module level
    globals()['User'] = User
    globals()['Issue'] = Issue
    # globals()['Comment'] = Comment


# Correct the syntax for __all__
__all__ = ['db', 'User', 'Issue', 'Comment']
