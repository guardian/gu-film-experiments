import webapp2
from webapp2 import abort
import jinja2
import os
import json
import logging
from urllib import quote, urlencode
from google.appengine.api import urlfetch

import headers

from models import StarReview

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), "templates")))

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

		headers.json(self.request)
		headers.cors(self.request)
		self.response.out.write(json.dumps(data))

app = webapp2.WSGIApplication([('/api/star-review', StarReviewHandler)],
                              debug=True)