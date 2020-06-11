import os
from unittest import TestCase

from models import db, User, Message, Follows, Likes

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

from app import app

db.create_all()

USER_DATA_1 = {
    "username": "test_user",
    "email": "test1@test.com",
    "password": "password",
    "image_url": None
}

USER_DATA_2 = {
    "username": "test_user_2",
    "email": "test2@test.com",
    "password": "password",
    "image_url": None
}

class UserModelViewCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        
    def tearDown(self):
        """Remove test client and sample data"""
        db.session.rollback()

    def test_show_user_loggedin(self):
        with app.test_client() as client:

            u1 = User(**USER_DATA_1)
            db.session.add(u1)
            db.session.commit()
            self.u1 = u1

            response = client.get("/users/1")

            self.assertEqual(response.status_code, 200)

    def test_show_user_loggedout(self):
        with app.test_client() as client:

            response = client.get("/users/1")

            self.assertEqual(response.status_code, 404)
