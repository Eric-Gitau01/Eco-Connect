import unittest
from app import create_app, db
from app.models.user import User
from werkzeug.security import generate_password_hash
import jwt
from datetime import datetime, timedelta
from flask import current_app
import uuid


class AuthTestCase(unittest.TestCase):
    def setUp(self):
        """Set up test app and database."""
        self.app = create_app('testing')
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()
            self.user = User(
                username='testuser',
                password=generate_password_hash('password123'),
                email='testuser@example.com'
            )
            db.session.add(self.user)
            db.session.commit()
            self.secret_key = current_app.config['SECRET_KEY']
            

    def tearDown(self):
        """Tear down test database."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    # Test user registration
    def test_register_user(self):
        """Test user registration endpoint."""
        response = self.client.post('/api/auth/register', json={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'password123'
        })
        data = response.get_json()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['message'], 'User created successfully')

        # ensure app context is active when querying the database
        with self.app.app_context():
            self.assertIsNotNone(User.query.filter_by(username='newuser').first())

    def test_register_existing_user(self):
        """Test registering an existing user."""
        self.client.post('/api/auth/register', json={
            'username': 'testuser',
            'email': 'irukangendo@gmail.com',
            'password': 'password123'
        })

        response = self.client.post('/api/auth/register', json={
            'username': 'testuser',
            'email': 'irukangendo@gmail.com',
            'password': 'password123'
        })

        data = response.get_json()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], 'User already exists'
        ' with the provided username or email')


    # Test user login
    def test_login_user(self):
        """Test login with valid credentials."""
        response = self.client.post('/api/auth/login', json={
            'username': 'testuser',
            'password': 'password123'
        })
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', data)
        self.assertIn('refresh_token', data)
        self.assertEqual(data['message'], 'Login successful')

    def test_login_invalid_credentials(self):
        """Test login with wrong password."""
        response = self.client.post('/api/auth/login', json={
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        data = response.get_json()

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['message'], 'Invalid credentials')

    # Test refresh token
    def test_refresh_token(self):
        """Test refreshing access token with valid refresh token."""
        with self.app.app_context():
            refresh_token = str(uuid.uuid4())
            self.user.refresh_token = refresh_token
            db.session.add(self.user)
            db.session.commit()

            # Verify token was saved in the database
            user_in_db = User.query.filter_by(id=self.user.id).first()
            assert user_in_db.refresh_token == refresh_token, "Refresh token not saved in the database"

        # Make a request to refresh token endpoint
        response = self.client.post('/api/auth/refresh-token', json={
            'refresh_token': refresh_token
        })
        data = response.get_json()

        # Check if the response is successful and contains the new access token
        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', data)

    def test_refresh_token_invalid(self):
        """Test refresh with an invalid token."""
        response = self.client.post('/api/auth/refresh-token', json={
            'refresh_token': 'invalid-token'
        })
        data = response.get_json()

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['message'], 'Invalid refresh token')



if __name__ == '__main__':
    unittest.main()
