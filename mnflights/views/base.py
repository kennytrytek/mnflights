from webapp2 import RequestHandler


class BaseRequestHandler(RequestHandler):
    def get(self):
        html = (
            '<head></head><body><p>Hello, junior.</p></body>'
        )
        self.response.write(html)
