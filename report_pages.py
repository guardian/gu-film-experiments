import webapp2
import jinja2
import os
import json
import logging
import handlers
import components
from urllib import quote, urlencode
from collections import namedtuple
from operator import attrgetter

from google.appengine.api import urlfetch

from models import StarReview, StarReviewSummary

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), "templates")))


class FilmReports(webapp2.RequestHandler):
	def get(self):
		template = jinja_environment.get_template('reports.html')

		summaries = sorted([s for s in StarReviewSummary.query()], key=attrgetter('average_rating'), reverse=True)

		template_values = {"reviews" : summaries}

		self.response.out.write(template.render(template_values))

app = webapp2.WSGIApplication([webapp2.Route(r'/reports/film', handler=FilmReports),
    ],
    debug=True)