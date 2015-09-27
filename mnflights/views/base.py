import os

import webapp2
from google.appengine.ext.webapp import template
from webapp2_extras import sessions


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
        root_dir = os.path.dirname(os.path.dirname(__file__))
        path = os.path.join(root_dir, 'templates', template_file_name)
        self.response.out.write(template.render(path, template_values))


class TemplateRequestHandler(BaseRequestHandler, TemplateMixin):
    pass
