import webapp2
from webapp2 import abort
import jinja2
import os
import json
import logging
from urllib import quote, urlencode
from collections import namedtuple
from operator import attrgetter

from google.appengine.api import urlfetch

import headers

from models import StarReview, StarReviewSummary

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), "templates")))

def summary_model_to_dict(summary):
	return {
		"movie_id" : summary.movie_id,
		"average_rating" : summary.average_rating,
		"max_rating" : summary.max_rating,
		"min_rating" : summary.min_rating,
		"ratings" : summary.ratings,
	}

class StarReviewHandler(webapp2.RequestHandler):
	def post(self):

		stars = self.request.POST.get('stars', None)
		movie_id = self.request.POST.get('movie_id', None)

		if not (stars and movie_id):
			abort(400, "Parameters not supplied")

		try:
			stars = int(stars)
			if not (0 < stars < 6):
				abort(400, "Star rating must be between 1 and 5")
		except ValueError:
			abort(400, "Need a numeric value for stars")

		data = {
			'ip_address' : self.request.remote_addr,
			'stars' : stars,
			'movie_id' : movie_id
			}

		query = StarReview.query(StarReview.movie_id == movie_id, StarReview.ip_address == self.request.remote_addr)

		if not query.iter().has_next():
			StarReview(movie_id=movie_id, stars=stars, ip_address=self.request.remote_addr).put()
		else:
			current_review = query.iter().next()
			current_review.stars = stars
			current_review.put()

		reviews = StarReview.query(StarReview.movie_id == movie_id)

		ratings = [review.stars for review in reviews]
		summary = StarReviewSummary(movie_id=movie_id,
			average_rating = sum(ratings) / len(ratings),
			max_rating = max(ratings),
			min_rating = min(ratings),
			ratings = len(ratings))
		summary.put()

		logging.info(summary)

		data['summary'] = summary_model_to_dict(summary)

		headers.json(self.request)
		headers.cors(self.request)
		self.response.out.write(json.dumps(data))

app = webapp2.WSGIApplication([('/api/star-review', StarReviewHandler)],
                              debug=True)