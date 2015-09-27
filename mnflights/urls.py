from webapp2 import Route

from .views.home import HomeRequestHandler
from .views.login import LoginRequestHandler

view_endpoints = [
    Route('/', handler=HomeRequestHandler),
    Route('/login', handler=LoginRequestHandler)
]
