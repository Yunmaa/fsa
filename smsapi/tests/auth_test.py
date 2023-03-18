import unittest
from smsapi import create_app
from config import TestConfig
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash
from smsapi.exts import db
from smsapi.models import User


class TestAuth(unittest.TestCase):

    def setUp(self):
        # Create a test smsapi
        self.app = create_app(config=TestConfig)

        # create an smsapi context
        self.app_contxt = self.app.app_context()
        self.app_contxt.push()
        self.client = self.app.test_client()

        # Create a test database
        db.create_all()

        # Create some test data
        self.user_data = {
            'email': 'test@example.com',
            'password': 'password123'
        }
        self.access_token = create_access_token(identity=1)

    # Clear the test database
    def tearDown(self):
        db.drop_all()

        self.app_contxt.pop()
        self.app = None
        self.client = None

    def test_login(self):
        # Extract the user details from the user_data dictionary
        email = self.user_data['email']
        password = self.user_data['password']

        # create a new instance of the User class for testing
        user = User(email=email, password_hash=password)
        user.set_password(password)

        # commit the new user data
        db.session.add(user)
        db.session.commit()

        # test the response from the login endpoint as 200
        response = self.client.post('/auth/login', json=self.user_data)
        self.assertEqual(response.status_code, 200)

    def test_registration(self):
        response = self.client.post('/auth/register', json=self.user_data)
        self.assertEqual(response.status_code, 201)

    def test_protected_route_with_valid_token(self):
        # Extract the user details from the user_data dictionary
        email = self.user_data['email']
        password = self.user_data['password']

        # create a new instance of the User class for testing
        user = User(email=email, password_hash=password)
        user.set_password(password)

        # commit the new user data
        db.session.add(user)
        db.session.commit()

        # Make a request to the protected route
        response = self.client.get('/auth/protected', headers={
            'Authorization': f'Bearer {self.access_token}'
        })