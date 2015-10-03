import re
import uuid

from .base import TemplateRequestHandler
from ..auth.api import obfuscate
from ..auth.models import User


class LoginRequestHandler(TemplateRequestHandler):
    def get(self):
        self.render_template('login.html', {})

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        user = User.get_by_id(username)
        if not user or user.password_hash != obfuscate(password):
            if 'session_id' in self.session:
                del self.session['session_id']
                self.session_store.save_sessions(self.response)
            self.redirect('/login')
            return

        self.session['user_id'] = user.key.urlsafe()
        self.session['session_id'] = uuid.uuid4().hex
        self.session_store.save_sessions(self.response)
        self.redirect('/')


class CreateAccountHandler(TemplateRequestHandler):
    def get(self, err_msg=''):
        self.render_template('create_account.html', {'err_msg': err_msg})

    def post(self):
        email = self.request.get('email', '')
        email_re = r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'
        if not re.match(email_re, email):
            self.get(err_msg='Invalid email address.')
            return

        if User.get_by_id(email):
            err_msg = (
                '{} already exists. Please enter a different email address.')
            self.get(err_msg=err_msg.format(email))
            return

        firstname = self.request.get('firstname', '').strip()
        lastname = self.request.get('lastname', '').strip()
        if not firstname and lastname:
            self.get(err_msg='Must provide first and last name.')
            return

        username = ' '.join([firstname, lastname])

        password = self.request.get('password', '')
        verify = self.request.get('verifypassword', '')
        if password != verify:
            self.get(err_msg='Passwords do not match.')
            return

        if len(password) < 6:
            self.get(err_msg='Password must be longer than five characters.')
            return

        User.create(email, username, password)
        self.redirect('/login')
