import logging
from graphene import Schema
import mal_service
import webapp2
import gtypes
import json

schema = Schema(query=gtypes.Query)

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('hello :)')

class GqlQuery(webapp2.RequestHandler):
    def post(self):
        self.response.headers['Content-Type'] = 'text/json'
        result = schema.execute(self.request.body)
        self.response.write(json.dumps(result.data))

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/query', GqlQuery)
], debug=True)
