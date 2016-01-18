from .base import TemplateRequestHandler


class HomeRequestHandler(TemplateRequestHandler):
    def get(self):
        user = self.get_user()

        from random import randint
        from ..golf.models import Hole

        holes = []
        for i in range(1, 10):
            holes.append(Hole(i, par=randint(3, 5)))

        data = {
            'name': user.name,
            'holes': holes}

        self.render_template('home.html', data)

    def post(self):
        self.response.write(self.request.body)
