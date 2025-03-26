from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

# This function will be called during app creation
def init_models():
    from app.models.user import User
    from app.models.issue import Issue
    from app.models.comment import Comment
    
    # Make these models available at the module level
    globals()['User'] = User
    globals()['Issue'] = Issue
    globals()['Comment'] = Comment

    # # Ensure database tables exist
    # db.create_all()

    # #check if users tables is empty before seeding
    # if not User.query.first():
    #     dummy_user = [
    #         {"username": "Daisy", "password": "123456"},
    #         {"username": "John", "password": "234567"},
    #         {"username": "Jane", "password": "345678"}
    #     ]

    #     for user in dummy_user:
    #         user = User(username=user_data['username'])
    #         user.set_password(user_data['password'])
    #         db.session.add(user)

    #     db.session.commit()
    #     print("Dummy users added.")
    # else:
    #     print("Users already exist")

# Correct the syntax for __all__
__all__ = ['db', 'User', 'Issue', 'Comment']
