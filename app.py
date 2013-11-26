import webapp2
import jinja2
import os
import json
import logging
import handlers
from urllib import quote, urlencode

from google.appengine.api import urlfetch

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), "templates")))

class MainPage(webapp2.RequestHandler):
	def get(self):
		template = jinja_environment.get_template('index.html')
		
		template_values = {}

		self.response.out.write(template.render(template_values))

app = webapp2.WSGIApplication([('/', MainPage),
                                webapp2.Route(r'/reviews/stars/<max_or_min>/<star_value>', handler = handlers.StarRated),
                                webapp2.Route(r'/reviews/stars/<star_value>', handler = handlers.StarRated)],
                              debug=True)