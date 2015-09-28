import webapp2
from jinja2 import Environment, PackageLoader
from webapp2_extras import sessions

env = Environment(loader=PackageLoader('mnflights', 'templates'))


class BaseRequestHandler(webapp2.RequestHandler):
    def dispatch(self):
        self.session_store = sessions.get_store(request=self.request)
        if not self.session.get('session_id'):
            if (not self.request.path.endswith('/login') and not
                    (self.request.referer or '').endswith('/login')):
                self.redirect('/login')
                return
        super(BaseRequestHandler, self).dispatch()

    @webapp2.cached_property
    def session(self):
        return self.session_store.get_session(max_age=3600 * 24)


class TemplateMixin(object):
    def render_template(self, template_file_name, template_values):
        template = env.get_template(template_file_name)
        self.response.out.write(template.render(template_values))


class TemplateRequestHandler(BaseRequestHandler, TemplateMixin):
    pass
