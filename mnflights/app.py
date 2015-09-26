from webapp2 import WSGIApplication

from .urls import view_endpoints

endpoints = []
endpoints += view_endpoints

app = WSGIApplication(endpoints, debug=True)
