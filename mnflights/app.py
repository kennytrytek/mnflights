from webapp2 import WSGIApplication

from .urls import view_endpoints

endpoints = []
endpoints += view_endpoints

config = {'webapp2_extras.sessions': {
    'secret_key': 'fb2bedbd695a42b7936824400eb40c38'}}

app = WSGIApplication(endpoints, config=config, debug=True)
