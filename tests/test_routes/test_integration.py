# tests/test_routes/test_integration.py

import unittest
from app import create_app, db
from sqlalchemy import inspect
from app.models.user import User
from app.models.issue import Issue
from app.models.comment import Comment
from werkzeug.security import generate_password_hash, check_password_hash


class IntegrationTestCase(unittest.TestCase):
    def setUp(self):
        """Set up the test client and initialize the database."""
        self.app = create_app('testing')
        self.client = self.app.test_client()
        with self.app.app_context():
            print('Drop all tables')
            db.drop_all()
            print('Create all tables')
            db.create_all()
            inspector = inspect(db.engine)
            print('Tables created: ', inspector.get_table_names())


            # Create a test user
            self.user = User(username='testuser', email='test@example.com')
            self.user.set_password('password')
            db.session.add(self.user)
            db.session.commit()
            print('Added test user:', self.user)


            # Log in to get token
            response = self.client.post('/api/auth/login', json={
                'email': 'test@example.com',
                'password': 'password'
            })
            print('login response:', response.json)
            self.token = response.json.get('access_token')

    def tearDown(self):
        """Clean up after each test."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
            db.engine.dispose()

    def test_create_issue_and_add_comment(self):
        """Test user can create an issue and add a comment."""
        # Create an issue
        response = self.client.post('/api/issues/', json={
            'title': 'Test Issue',
            'description': 'This is a test issue',
            'user_id': self.user.id,
            'location': 'Nairobi'
        }, headers={'Authorization': f'Bearer {self.token}'})

        
        print('Response status:', response.status_code)
        print('Response:', response.json)

        # Check that the issue was created successfully
        self.assertEqual(response.status_code, 201)

        #correctly extract the id from the response key: {response.json}')
        self.assertIn('id', response.json['Issue'], msg=f'Response does not contain id key: {response.json["Issue"]}')
        issue_id = response.json['Issue']['id']
        self.assertIsInstance(issue_id, int, msg=f'Issue id is not an integer: {issue_id}') 


        # Add a comment to the issue
        response = self.client.post('/api/comments/', json={
            'content': 'Test comment',
            'user_id': self.user.id,
            'issue_id': issue_id
        }, headers={'Authorization': f'Bearer {self.token}'})
        print('Comment response status:', response.status_code)
        print('Comment response:', response.json)

        # Check that the comment was added successfully
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['message'], 'Comment added successfully')

        # Check that the comment is in the database
        with self.app.app_context():
            comment = Comment.query.filter_by(content='Test comment').first()
            self.assertIsNotNone(comment)
            self.assertEqual(comment.issue_id, issue_id)


    if __name__ == '__main__':
        unittest.main()
