from webtest import TestApp

from ...app import app
from ...auth.models import User
from ...utils import DatastoreTestCase


class PostTestCase(DatastoreTestCase):
    def setUp(self):
        super(PostTestCase, self).setUp()
        self.app = TestApp(app)

    def test_successful_login(self):
        User.create('ThePope', 'this is my password')
        data = {
            'username': 'ThePope',
            'password': 'this is my password'}
        resp = self.app.post('/login', data, headers={'referer': '/login'})
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.location, 'http://localhost/')

    def test_unsuccessful_login_bad_user(self):
        data = {
            'username': 'ThePope',
            'password': 'this is not my password'}
        resp = self.app.post('/login', data)
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.location, 'http://localhost/login')

    def test_unsuccessful_login_bad_password(self):
        User.create('ThePope', 'this is my password')
        data = {
            'username': 'ThePope',
            'password': 'this is not my password'}
        resp = self.app.post('/login', data)
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.location, 'http://localhost/login')
