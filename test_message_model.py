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


class MessageModelTestCase(TestCase):

    def setUp(self):
        db.drop_all()
        db.create_all()

        User.query.delete()
        Message.query.delete()

        self.client = app.test_client()

    def tearDown(self):
        db.session.rollback()

    def test_message_model(self):
        User.query.delete()
        Message.query.delete()

        u1 = User.signup(
            email="test1@test.com",
            username="test1user",
            password="HASHED_PASSWORD",
            image_url=None
        )

        test_message = Message(text="This is a test message.", user_id=1)

        db.session.add(test_message)
        db.session.commit()

        self.assertEqual(len(u1.messages), 1)
        self.assertEqual(u1.messages[0].text, "This is a test message.")

    def test_liked_message(self):
        User.query.delete()
        Message.query.delete()

        u1 = User.signup(
            email="test1@test.com",
            username="test1user",
            password="HASHED_PASSWORD",
            image_url=None
        )

        test_message = Message(text="This is a test message.", user_id=1)
        test_message_2 = Message(text="Did I liked this message?", user_id=1)

        db.session.add_all([u1, test_message, test_message_2])
        u1.likes.append(test_message)

        db.session.commit()

        self.assertEqual(len(u1.likes), 1)
        likes = [message.id for message in u1.likes]
        self.assertEqual(test_message_2.id in likes, False)

