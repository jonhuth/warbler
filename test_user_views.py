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
            with client.session_transaction() as session:
                session['CURR_USER_KEY'] = 1

            u1 = User(**USER_DATA_1)
            db.session.add(u1)
            db.session.commit()
            self.u1 = u1

            response = client.get("/users/1")

            self.assertEqual(response.status_code, 200)
            self.assertEqual(session['CURR_USER_KEY'], 1)
            # self.assertIn(response, )

    def test_add_message(self):
        with app.test_client() as client:
            with client.session_transaction() as session:
                session['CURR_USER_KEY'] = 1

            u1 = User(**USER_DATA_1)
            db.session.add(u1)
            db.session.commit()
            self.u1 = u1

            response = client.post("/messages/new", data={"text":"This is a test message.", "user_id":"1"})
            html = response.get_data(as_text=True)

            self.assertEqual(len(u1.messages), 0)


    def test_show_user_loggedout(self):
        with app.test_client() as client:
            with client.session_transaction() as session:
                session['CURR_USER_KEY'] = None

            u1 = User(**USER_DATA_1)
            db.session.add(u1)
            db.session.commit()
            self.u1 = u1

            response = client.get("/messages/new")

            self.assertEqual(response.status_code, 302)
            # assert in the redirect page , some html part

            test_message = Message(text="This is a test message.", user_id=u1.id)
            u1.messages.append(test_message)

            self.assertEqual(len(u1.messages), 1)


    def test_delete_message_loggedin(self):
        with app.test_client() as client:
            with client.session_transaction() as session:
                session['CURR_USER_KEY'] = 1

            u1 = User(**USER_DATA_1)
            db.session.add(u1)
            db.session.commit()
            self.u1 = u1

            test_message = Message(text="This is a test message.", user_id=u1.id)
            u1.messages.append(test_message)
            db.session.commit()

            response = client.post(f'/messages/{test_message.id}/delete', follow_redirects=True)

            db.session.delete(test_message)
            db.session.commit()

            self.assertEqual(response.status_code, 200)

    # def test_delete_message_loggedout(self):
    #     with app.test_client() as client:
    #         with client.session_transaction() as session:
    #             session['CURR_USER_KEY'] = None

    #         u1 = User(**USER_DATA_1)
    #         db.session.add(u1)
    #         db.session.commit()
    #         self.u1 = u1

    #         response = client.get("/logout")

    #         self.assertEqual(response.status_code, 302)

