from .base import TemplateRequestHandler


class HomeRequestHandler(TemplateRequestHandler):
    def get(self):
        self.render_template('home.html', {'name': 'George'})
