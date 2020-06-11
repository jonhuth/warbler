"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User, Message, Follows, Likes

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()
    def tearDown(self):
        """Remove test client and sample data"""
        db.session.rollback()

    def test_user_model(self):
        """Does basic model work?"""
        User.query.delete()
        u1 = User(
            email="test1@test.com",
            username="test1user",
            password="HASHED_PASSWORD"
        )
        u2 = User(
            email="test2@test.com",
            username="test2user",
            password="HASHED_PASSWORD"
        )

        db.session.add_all([u1, u2])
        u1.following.append(u2)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u1.messages), 0)
        self.assertEqual(len(u1.followers), 0)
        self.assertEqual(str(u1), "<User #1: test1user, test1@test.com>")
        self.assertEqual(u1.is_following(u2), True)
        self.assertEqual(u2.is_following(u1), False)
        self.assertEqual(u2.is_followed_by(u1), True)
        self.assertEqual(u1.is_followed_by(u2), False)
        
        User.signup('test3user', 'test3@test.com', 'HASHED_PASSWORD', None)
        self.assertEqual(len(User.query.all()), 3)
        # todo: test trying to signup invalid user, handle error in test
        # User.signup('test3', None, 'password', None)
        # self.assertEqual(len(User.query.all()), 3)
        
        
    def test_user_model_auth(self):
        User.signup('test1user', 'test1@test.com', 'HASHED_PASSWORD', None)
        
        db.session.commit()

        test_user_auth1 = User.authenticate('test1user', 'HASHED_PASSWORD')
        test_user_auth2 = User.authenticate('test2user', 'HASHED_PASSWORD')
        test_user_auth3 = User.authenticate('test1user', 'hased_Password')

        self.assertEqual(str(test_user_auth1), "<User #1: test1user, test1@test.com>")
        self.assertEqual(test_user_auth2, False)
        self.assertEqual(test_user_auth3, False)
