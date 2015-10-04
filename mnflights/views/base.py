import webapp2
from google.appengine.ext import ndb
from jinja2 import Environment, PackageLoader
from webapp2_extras import sessions

env = Environment(loader=PackageLoader('mnflights', 'templates'))


class UserMixin(object):
    def get_user(self):
        return ndb.Key(urlsafe=self.session['user_id']).get()


class BaseRequestHandler(webapp2.RequestHandler, UserMixin):
    def dispatch(self):
        self.session_store = sessions.get_store(request=self.request)
        if not self.session.get('session_id'):
            no_auth = ('/login', '/create_account', '/forgot_password',
                       '/create_new_password')
            if (self.request.path not in no_auth and
                    not (self.request.referer or '').endswith('/login')):
                self.redirect('/login')
                return

        super(BaseRequestHandler, self).dispatch()

    @webapp2.cached_property
    def session(self):
        return self.session_store.get_session(max_age=3600 * 24)


class TemplateMixin(object):
    def render_template(
            self, template_file_name, template_values, write_response=True):
        template = env.get_template(template_file_name)
        rendered = template.render(template_values)
        if write_response:
            self.response.out.write(rendered)
        else:
            return rendered


class TemplateRequestHandler(BaseRequestHandler, TemplateMixin):
    pass
