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

		def ratings_reducer(summaries, review):
			logging.info(summaries)
			if not review.movie_id in summaries:
				summaries[review.movie_id] = [review.stars]
				return summaries

			summaries[review.movie_id].append(review.stars)

			return summaries

		ratings = reduce(ratings_reducer, reviews, {})

		def summary_gen(movie_id, ratings_list):

			return Summary(movie_id, sum(ratings_list) / len(ratings_list), max(ratings_list), min(ratings_list), len(ratings_list))

		summaries = [summary_gen(k, v) for k,v in ratings.items()]
		summaries = sorted(summaries, key=attrgetter('average_rating'), reverse=True)

		logging.info(summaries)

		template_values = {"reviews" : summaries}

		self.response.out.write(template.render(template_values))

app = webapp2.WSGIApplication([webapp2.Route(r'/reports/film', handler=FilmReports),
    ],
    debug=True)