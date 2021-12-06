from os import lseek
from unittest import TestCase
from server import app
from model import connect_to_test_db, db
# from model_test import connect_to_db, db
from flask import session


class FlaskTestsBasic(TestCase):
    """Flask tests."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True
        with self.client as c:
            with c.session_transaction() as sess:
                sess['email'] = "test1@gmail.com"

    def test_home_page(self):
        """Test homepage page."""

        result = self.client.get("/")
        self.assertIn(b"Civic Engagement", result.data)

    def test_record_service_page(self):
        """Test Record Service page."""

        result = self.client.get("/client_page")
        self.assertIn(b"Client Demographic", result.data)
        self.assertIn(b"Add service notes", result.data)

    def test_record_service_page(self):
        """Test Record Service page."""

        result = self.client.get("/show_search_box")
        self.assertIn(b"Client Search", result.data)
        self.assertIn(b"Search", result.data)

class FlaskTestsDatabase(TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()
        app.config['TESTING'] = True
        with self.client as c:
            with c.session_transaction() as sess:
                sess['query_option'] = 0
        # Connect to test database
        connect_to_test_db(app, "postgresql:///testdb")
        
        # I did it from command lines
        # db.create_all()
        # example_data()

    def tearDown(self):
        """Do at end of every test."""

        db.session.remove()
        # Don't call drop_all since I don't run example_data on line 54 when I run this test
        # db.drop_all()
        db.engine.dispose()

    def test_login(self):
            """Test login page."""

            result = self.client.post("/login",
                                    data={"email": "test1@gmail.com", "password": "test1"},
                                    follow_redirects=True)
            self.assertIn(b"Client Search", result.data)
            self.assertIn(b"Search", result.data)

    def test_run_query_list_1(self):
            """Test run_query route query_id = 1 """

            with self.client as c:
                with c.session_transaction() as sess:
                    sess['email'] = "test1@gmail.com"

            result = self.client.get("/run_query/1",
                                      query_string={"query_option" : "1"},
                                      follow_redirects=False)
            self.assertIn(b"Second Harvest Clients", result.data)
            
    def test_run_query_list_2(self):
            """Test run_query route query_id = 2 """

            with self.client as c:
                with c.session_transaction() as sess:
                    sess['email'] = "test1@gmail.com"
            result = self.client.get("/run_query/2",
                                      query_string={"query_option" : "2"},
                                      follow_redirects=False)

            # This table should be empty since there are clients in this program
            self.assertNotIn(b"Elders Program Clients", result.data)

    def test_run_query_list_3(self):
            """Test run_query route query_id = 3 """

            with self.client as c:
                with c.session_transaction() as sess:
                    sess['email'] = "test1@gmail.com"

            result = self.client.get("/run_query/3",
                                      query_string={"query_option" : "3"},
                                      follow_redirects=False)
            self.assertIn(b"Health Care Clients", result.data)

# class FlaskTestsLoggedIn(TestCase):
#     """Flask tests with user logged in to session."""

#     def setUp(self):
#         """Stuff to do before every test."""

#         app.config['TESTING'] = True
#         app.config['SECRET_KEY'] = 'key'
#         self.client = app.test_client()

#         with self.client as c:
#             with c.session_transaction() as sess:
#                 sess['user_id'] = 1

#     def test_important_page(self):
#         """Test important page."""

#         login_email = self.client.get("/login")
#         self.assertIn(b"test1@gmail.com", login_email)


class FlaskTestsLoggedOut(TestCase):
    """Flask tests with user logged in to session."""

    def setUp(self):
        """Stuff to do before every test."""

        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_logout(self):
        """Test that user is sent back to home page when logged out
           and is blocked from running Search route """

        result = self.client.get("/")
        self.assertIn(b"Civic Engagement", result.data)
        result = self.client.get("/show_search_box")
        self.assertNotIn(b"Client Search", result.data)
        self.assertNotIn(b"Search", result.data)
       
class FlaskTestsLogInLogOut(TestCase):  # Bonus example. Not in lecture.
    """Test log in and log out."""

    def setUp(self):
        """Before every test"""

        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_login(self):
        """Test log in form.
        Unlike login test above, 'with' is necessary here in order to refer to session.
        """

        with self.client as c:
            result = c.post('/login',
                            data={'email': 'test1@gmail.com', 'password': 'test1'},
                            follow_redirects=True
                            )
            self.assertEqual(session['email'], 'test1@gmail.com')

    def test_logout(self):
        """Test logout route."""

        with self.client as c:
            with c.session_transaction() as sess:
                sess['email'] = 'test1@gmail.com'

            result = self.client.get('/logout', follow_redirects=True)

            self.assertNotIn(b'email', session)
            self.assertIn(b'Civic Engagement', result.data)


if __name__ == "__main__":
    import unittest
    unittest.main()
