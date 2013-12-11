import webapp2
import logging
import headers
import json

from google.appengine.api import memcache

import film_reviews

class StarRated(webapp2.RequestHandler):
    def get(self, max_or_min=None, star_value=None):
        filtered_reviews = film_reviews.filtered_reviews(max_or_min, star_value)
        logging.info(filtered_reviews)
        headers.json(self.response)
        headers.cache(self.response, 60)
        headers.cors(self.response)
        self.response.out.write(json.dumps(filtered_reviews))
