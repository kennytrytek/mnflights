from google.appengine.ext import ndb
from webapp2 import WSGIApplication

from .urls import view_endpoints

endpoints = []
endpoints += view_endpoints


class SecretKey(ndb.Model):
    value = ndb.StringProperty(indexed=False)

config = {'webapp2_extras.sessions': {
    'secret_key': str(ndb.Key('SecretKey', 1).get().value)}}

app = WSGIApplication(endpoints, config=config, debug=True)
