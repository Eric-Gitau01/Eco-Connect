import unittest
from app import create_app, db
from app.models.user import User
from app.models.issue import Issue

class IssuesTestCase(unittest.TestCase):
    """Test case for issue routes"""

    def setUp(self):
        """Set up test variables and app context."""
        self.app = create_app('testing')
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()
            
            #create a test user and ensure it is in the database
            test_user = User(username='test_user', email='test@example.com', password_hashed='password')
            db.session.add(test_user)
            db.session.commit()

            # Assign user id to test_user_id
            self.test_user_id = test_user.id

            # Sample issue data
            self.new_issue = {
                'title': 'Test Issue',
                'location': 'Kirinyaga County',
                'description': 'This is a test issue',
                'user_id': self.test_user_id
            }


    def tearDown(self):
        """Clear test database."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    # Test issue creation
    def test_create_issue(self):
        response = self.client.post('/api/issues/', json=self.new_issue)
        data = response.get_json()
        self.assertEqual(response.status_code, 201)
        self.assertIn('Issue created successfully', data['message'])
        self.assertEqual(data['Issue']['title'], self.new_issue['title'])
        self.assertEqual(data['Issue']['location'], self.new_issue['location'])
        self.assertEqual(data['Issue']['description'], self.new_issue['description'])
    

    # Test fetching an issue
    def test_get_issue(self):
        with self.app.app_context():
            # add issue to database
            issue = Issue(**self.new_issue)
            db.session.add(issue)
            db.session.commit()

            # refresh the issue instance to get the id
            db.session.refresh(issue)

            # ensure the issue exists
            self.assertIsNotNone(issue.id)

            # get the issue by id
            response = self.client.get(f'/api/issues/{issue.id}')
            data = response.get_json()

            # verify the response
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data['id'], issue.id)
            self.assertEqual(data['title'], self.new_issue['title'])
            self.assertEqual(data['location'], self.new_issue['location'])
            self.assertEqual(data['description'], self.new_issue['description'])
            


    # Test updating an issue
    def test_update_issue(self):
        # Add issue to database
        with self.app.app_context():
            issue = Issue(**self.new_issue)
            db.session.add(issue)
            db.session.commit()

            # Refresh the issue instance to get the id
            db.session.refresh(issue)

            # Ensure the issue exists
            self.assertIsNotNone(issue.id)

            # Update the issue
            updated_data = {
                'title': 'Updated Title',
                'location': 'Updated location',
                'description': 'Updated description'
                
                }
            
            # send the update request
            response = self.client.put(f'/api/issues/{issue.id}', json=updated_data)
            data = response.get_json()

            # verify the response
            self.assertEqual(response.status_code, 200)
            self.assertIn('Issue updated successfully', data['message'])

        # updated_data = {
        #     'title': 'Updated Title',
        #     'description': 'Updated description',
        #     'location': 'Updated location'
        #     }
        # response = self.client.put(f'/api/issues/{issue.id}', json=updated_data)
        # data = response.get_json()
        # self.assertEqual(response.status_code, 200)
        # self.assertIn('Issue updated successfully', data['message'])

        # updated_issue = Issue.query.get(issue.id)
        # self.assertEqual(updated_issue.title, 'Updated Title')
        # self.assertEqual(updated_issue.description, 'Updated description')
        # self.assertEqual(updated_issue.location, 'Updated location')


    # Test deleting an issue
    def test_delete_issue(self):
        with self.app.app_context():
            issue = Issue(**self.new_issue)
            db.session.add(issue)
            db.session.commit()

            # Confirm issues exists before deleting
            self.assertIsNotNone(Issue.query.get(issue.id))

            # delete issue
            response = self.client.delete(f'/api/issues/{issue.id}')
            data = response.get_json()

            # Verify issue is deleted
            self.assertEqual(response.status_code, 200)
            self.assertIn('Issue deleted successfully', data['message'])

            # Confirm issue is deleted
            deleted_issue = Issue.query.get(issue.id)
            self.assertIsNone(deleted_issue)


if __name__ == '__main__':
    unittest.main()
