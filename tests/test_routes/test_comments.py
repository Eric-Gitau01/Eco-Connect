import unittest
from app import create_app, db
from app.models.comment import Comment
from app.models.user import User
from app.models.issue import Issue

class CommentsTestCase(unittest.TestCase):
    def setUp(self):
        """Set up a clean app and test database before each test."""
        self.app = create_app('testing')
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

            # Add a test user and issue
            test_user = User(
                username='test_user',
                email='test_user@example.com',
                password='password'
                )
            # Save the test user to the database
            db.session.add(test_user)
            db.session.commit()

            # Create a test issue
            test_issue = Issue(
                title='Test Issue',
                description='Test Description',
                user_id=test_user.id,
                location='Nairobi'
                )
            
            # Add the test user and issue to the database
            db.session.add_all([test_user, test_issue])
            db.session.commit()
            
            # Assign the test user and issue IDs to instance variables
            self.test_user_id = test_user.id
            self.test_issue_id = test_issue.id

    def tearDown(self):
        """Clear the database after each test."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_add_comment(self):
        """Test adding a new comment by its user ID and issue ID."""
        data = {
            'user_id': self.test_user_id,
            'issue_id': self.test_issue_id,
            'content': 'This is a test comment'
        }

        # Send a POST request to the comments endpoint
        response = self.client.post('/api/comments/', json=data, headers={'Content-Type': 'application/json'})
        self.assertEqual(response.status_code, 201)
        self.assertIn('Comment added successfully', response.json['message'])

    def test_get_comment(self):
        """Test retrieving a comment by its ID."""
        with self.app.app_context():
            comment = Comment(
                user_id=self.test_user_id,
                issue_id=self.test_issue_id,
                content='Sample comment'
                )
            
            # Add the comment to the database
            db.session.add(comment)
            db.session.commit()

            # Confirm the comment exists before fetching
            self.assertIsNotNone(Comment.query.get(comment.id))

            # Save the comment ID
            comment_id = comment.id
        
        # Send a GET request to the comments endpoint
        response = self.client.get(f'/api/comments/{comment.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['content'], 'Sample comment')


    def test_update_comment(self):
        """Test updating a comment's content."""
        with self.app.app_context():
            comment = Comment(
                user_id=self.test_user_id,
                issue_id=self.test_issue_id,
                content='Old comment')
            
            # Add the comment to the database
            db.session.add(comment)
            db.session.commit()

            # save the comment id
            comment_id = comment.id
            self.assertIsNotNone(Comment.query.get(comment_id)) 

            # Confirm the comment exists before updating
            self.assertIsNotNone(Comment.query.get(comment_id))
        
        # Send a PUT request to the comments endpoint
        updated_data = {'content': 'Updated comment'}
        response = self.client.put(f'/api/comments/{comment.id}', json=updated_data, headers={'Content-Type': 'application/json'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Comment updated successfully', response.json['message'])

    def test_delete_comment(self):
        """Test deleting a comment."""
        with self.app.app_context():
            comment = Comment(
                user_id=self.test_user_id,
                issue_id=self.test_issue_id,
                content='To be deleted')
            
            # Add the comment to the database
            db.session.add(comment)
            db.session.commit()

            # Confirm the comment exists before deleting
            self.assertIsNotNone(Comment.query.get(comment.id))
            comment_id = comment.id
        
        # Send a DELETE request to the comments endpoint
        response = self.client.delete(f'/api/comments/{comment.id}', headers={'Content-Type': 'application/json'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Comment deleted successfully', response.json['message'])

if __name__ == '__main__':
    unittest.main()
