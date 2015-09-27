from webapp2 import WSGIApplication

from .urls import view_endpoints

endpoints = []
endpoints += view_endpoints

config = {'webapp2_extras.sessions': {'secret_key': 'squidpants'}}

app = WSGIApplication(endpoints, config=config, debug=True)
