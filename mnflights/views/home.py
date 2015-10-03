from .base import TemplateRequestHandler


class HomeRequestHandler(TemplateRequestHandler):
    def get(self):
        user = self.get_user()
        self.render_template('home.html', {'name': user.name})
