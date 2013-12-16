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

from models import StarReview

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), "templates")))

class FilmReports(webapp2.RequestHandler):
	def get(self):
		template = jinja_environment.get_template('reports.html')
		
		reviews = StarReview.query()

		Summary = namedtuple('StarSummary', ['film_id', 'average_rating', 'max_rating', 'min_rating', 'ratings'])

		def summarise(summaries, review):
			if not review.movie_id in summaries:
				summaries[review.movie_id] = Summary(review.movie_id, review.stars, review.stars, review.stars, 1)

			return summaries
		summaries = reduce(summarise, reviews, {})
		summaries = sorted(summaries.values(), key=attrgetter('average_rating'), reverse=True)
		logging.info(summaries)

		template_values = {"reviews" : summaries}

		self.response.out.write(template.render(template_values))

app = webapp2.WSGIApplication([webapp2.Route(r'/reports/film', handler=FilmReports),
    ],
    debug=True)