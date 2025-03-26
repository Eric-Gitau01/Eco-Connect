import unittest
from app import create_app, db
from app.models.user import User

class UserModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_password_hashing(self):
        user = User(username='testuser')
        user.set_password('password123')
        self.assertFalse(user.check_password('wrongpassword'))
        self.assertTrue(user.check_password('password123'))

if __name__ == '__main__':
    unittest.main()
