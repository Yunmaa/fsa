import unittest
from smsapi import create_app
from config import TestConfig
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash

from smsapi.exts import db
from smsapi.models import Student


class StudentTestCase(unittest.TestCase):

    def setUp(self):
        # Create a test app
        self.app = create_app(config=TestConfig)

        # create an app context
        self.app_contxt = self.app.app_context()
        self.app_contxt.push()
        self.client = self.app.test_client()

        # Create the test database
        db.create_all()

    # Destroy the test database
    def tearDown(self):
        db.drop_all()

        # Remove the app_context and reset the test client
        self.app_contxt.pop()
        self.app = None
        self.client = None

    def test_get_all_students(self):
        # Create the access token and headers for the request
        token = create_access_token(identity='testadmin')

        headers = {"Authorization": f"Bearer {token}"}

        # send the response
        response = self.client.get('students', headers=headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'students': []})

    def test_get_one_student(self):
        token = create_access_token(identity='testadmin')

        headers = {"Authorization": f"Bearer {token}"}

        # Create a student to be queried from the databse
        student = Student(name='teststudent', email='testemail')
        db.session.add(student)
        db.session.commit()

        response = self.client.get('students', headers=headers)

        self.assertEqual(response.status_code, 200)

    def test_get_one_student_not_found(self):
        token = create_access_token(identity='testadmin')

        headers = {"Authorization": f"Bearer {token}"}

        response = self.client.get('students/1', headers=headers)

        self.assertEqual(response.status_code, 404)

    def test_get_all_courses(self):
        token = create_access_token(identity='testadmin')

        headers = {"Authorization": f"Bearer {token}"}

        response = self.client.get('courses', headers=headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])