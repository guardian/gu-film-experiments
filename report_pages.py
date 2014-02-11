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

		summaries = StarReviewSummary.query().order(-StarReviewSummary.average_rating, -StarReviewSummary.ratings)

		template_values = {"reviews" : summaries}

		self.response.out.write(template.render(template_values))

class EngagementReportHandler(webapp2.RequestHandler):
	def get(self):
		template = jinja_environment.get_template('engagement-report.html')

		ratings = StarReview.query().count()
		unique_ip_addresses = StarReview.query(projection=["ip_address"], distinct=True).count()

		template_values = {
			'ratings' : ratings,
			'ip_addresses' : unique_ip_addresses,
		}

		self.response.out.write(template.render(template_values))


app = webapp2.WSGIApplication([webapp2.Route(r'/reports/film', handler=FilmReports),
	webapp2.Route(r'/reports/film/engagement', handler=EngagementReportHandler),
    ],
    debug=True)