import unittest
from app import app, db
from models import User


class BloglyTestCase(unittest.TestCase):
    """Test casses for Blogly routes"""


    def setUp(self):
        """set up test enviroment and test data."""
        app.config['SQLACHEMY_DATABASE_URI'] = 'postgresql:///test_blogly'
        app.config['TESTING'] = True
        app.config['WTF_CSRFENABLED'] = False 
        self.client = app.test_client()

        with app.app_context():
            db.drop_all()
            db.create_all()


            # Add sample user for testing
            user = User(first_name="Test", last_name="User", img_url=None)
            db.session.add(user)
            db.session.commit()
    
    def tearDown(self):
        """clean up fouled database session"""
        with app.app_context():
            db.session.rollback()
            

    def test_user_listing(self):
            """Test the user listing route."""
            resp = self.client.get('/user')
            html = resp.data.decode()


            self.assertEqual(resp.status_code, 200)
            self.assertIn("Test User", html)

        
    def test_add_new_user(self):
            """Test adding a new user."""
            data = {
             "first_name": "New",
             "last_name": "User",
             "img_url": "https://example.com/image.png"
            }
            resp = self.client.post('/user/new', data=data, follow_redirects=True)
            html = resp.data.decode()
            

            self.assertEqual(resp.status_code, 200)
            self.assertIn("New User", html)


    def test_user_edit(self):
        """Test editing an existing user."""
        # Get the first user ID
        with app.app_context():
            user = User.query.first()
            data = {
                 "first_name": "Updated",
                "last_name": "User",
                "img_url": "https://example.com/updated_image.png"
            }
            resp = self.client.post(f'/user/{user.id}/edit', data=data, follow_redirects=True)
            html = resp.data.decode()


            self.assertEqual(resp.status_code, 200)
            self.assertIn("Updated User", html)


if __name__ == "__main__":
    unittest.main()