import re
import uuid

from google.appengine.ext import ndb
from google.appengine.api import mail

from .base import TemplateRequestHandler
from ..auth.api import obfuscate
from ..auth.models import PasswordResetToken, User


class LoginRequestHandler(TemplateRequestHandler):
    def get(self):
        self.render_template('login.html', {'hide_logout': True})

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


class LogoutRequestHandler(TemplateRequestHandler):
    def post(self):
        del self.session['user_id']
        del self.session['session_id']
        self.session_store.save_sessions(self.response)
        self.redirect('/')


class CreateAccountHandler(TemplateRequestHandler):
    def get(self, err_msg=''):
        self.render_template('create_account.html', {
            'err_msg': err_msg, 'hide_logout': True})

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


class ForgotPasswordHandler(TemplateRequestHandler):
    def get(self, err_msg=None):
        self.render_template('password/forgot_password.html', {
            'err_msg': err_msg, 'hide_logout': True})

    def post(self):
        email = self.request.get('email')
        try:
            user = User.get_by_id(email)
        except:
            user = None
        if not user:
            self.get(err_msg='User does not exist.')
            return

        token = uuid.uuid4().hex + uuid.uuid4().hex + uuid.uuid4().hex
        PasswordResetToken(id=user.key.urlsafe(), token=token).put()
        base_url = self.request.relative_url('/').rstrip('/')
        body = self.render_template(
            'password/password_reset_email.html',
            {'base_url': base_url,
             'token': token,
             'userid': user.key.urlsafe(),
             'raw': True},
            write_response=False)

        import logging
        logging.info(body)
        html_body = self.render_template(
            'password/password_reset_email.html',
            {'base_url': base_url,
             'token': token,
             'userid': user.key.urlsafe()},
            write_response=False)

        mail.send_mail(
            'jmarkeyburger@gmail.com',  # sender
            email,  # recipient
            'Monday Night Flights Password Reset',  # subject
            body,  # body
            html=html_body)  # html rendered body

        self.render_template('password/forgot_password.html', {
            'sent': 'Password reset email sent.',
            'hide_logout': True})


class CreateNewPasswordHandler(TemplateRequestHandler):
    def get(self, err_msg=None, show_form=False):
        userid = self.request.get('userid')
        tokenid = self.request.get('token')
        if err_msg:
            template_vals = {'err_msg': err_msg, 'hide_logout': True}
            if show_form:
                template_vals['userid'] = userid
                template_vals['token'] = tokenid

            self.render_template(
                'password/create_new_password.html', template_vals)
            return

        try:
            user = ndb.Key(urlsafe=userid).get()
            if not user:
                raise ValueError
        except:
            self.get(err_msg='Invalid password reset link.')
            return

        try:
            token = PasswordResetToken.get_by_id(userid)
            if not token or token.token != tokenid:
                raise ValueError
        except:
            self.get(err_msg='Expired or invalid password reset token.')
            return

        self.render_template('password/create_new_password.html', {
            'token': token.token, 'userid': userid, 'hide_logout': True})

    def post(self):
        password = self.request.get('password', '')
        verify = self.request.get('verifypassword', '')
        if password != verify:
            self.get(err_msg='Passwords do not match.', show_form=True)
            return

        if len(password) < 6:
            self.get(
                err_msg='Password must be longer than five characters.',
                show_form=True)
            return
        try:
            self.update_password(
                self.request.get('userid'),
                password,
                self.request.get('token'))
        except:
            self.get(err_msg='Could not update password. Please contact '
                             'the site administrator or try sending the '
                             'password reset email again.')
            return

        self.redirect('/login')

    @ndb.transactional(xg=True)
    def update_password(self, user_id, new_password, reset_token):
        user = ndb.Key(urlsafe=user_id).get()
        token = PasswordResetToken.get_by_id(user_id)
        if token.token != reset_token:
            raise ValueError('Tokens do not match')

        user.password_hash = obfuscate(new_password)
        user.put()
        token.key.delete()
