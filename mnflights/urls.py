from webapp2 import Route

from .views.home import HomeRequestHandler

view_endpoints = [
    Route('/', handler=HomeRequestHandler)
]
