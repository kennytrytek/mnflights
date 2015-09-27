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

        self.session['session_id'] = uuid.uuid4().hex
        self.session_store.save_sessions(self.response)
        self.redirect('/')
