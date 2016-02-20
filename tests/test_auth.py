import unittest

from app import app, db
from config import TestConfig
from app.auth import User


class AuthTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config.from_object(TestConfig)
        db.create_all()

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all()

    def setUp(self):
        self.app = app.test_client()

    def test_add_user(self):
        user = User(username='test@gmail.com', password='mysecret', first_name='chris', last_name='hall')
        db.session.add(user)
        db.session.commit()
        queried_user = User.query.filter_by(username='test@gmail.com').first()
        self.assertEqual(queried_user.username, 'test@gmail.com')
        self.assertNotEqual(queried_user.password, 'mysecret', 'Password not hashed')
        self.assertEqual(queried_user.first_name, 'chris')
        self.assertEqual(queried_user.last_name, 'hall')

    def test_password_hashing(self):
        user = User(username='test@gmail.com', password='mysecret', first_name='chris', last_name='hall')
        db.session.add(user)
        db.session.commit()
        queried_user = User.query.filter_by(username='test@gmail.com').first()
        self.assertTrue(queried_user.is_correct_password('mysecret'))

    def test_login_route(self):
        response = self.app.get('/login/')
        assert response.status_code == 200
