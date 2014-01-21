import os
import jinja2
import webapp2
import film_reviews
import logging
import random
import ratings

from models import StarReview, StarReviewSummary

jinja_environment = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), "templates")))

jinja_environment.filters['pluralize'] = ratings.pluralize

class BestAndWorstInCinema(webapp2.RequestHandler):
	def get(self, quantity):

		template = jinja_environment.get_template('bestandworstincinema.html')
		reviews = film_reviews.best_and_worst(int(quantity))

		for r in reviews:
			contributors = []
			tags = r.get('tags')
			for tag in tags:
				if tag.get('type') == 'contributor':
					contributors.append(tag.get('webTitle'))
					r['contributors'] = " ".join(contributors)

		self.response.out.write(template.render({'reviews':reviews}))

class StarReviewHandler(webapp2.RequestHandler):
	def get(self, film_id):
		template = jinja_environment.get_template('star-review.html')


		template_values = {
			'film_id' : film_id,
			'star_values' : range(1, 6),
			'current_stars' : None,
			'ratings_summary' : {'average_rating': 0, 'ratings': 0},
		}

		query = StarReview.query(StarReview.movie_id == film_id, StarReview.ip_address == self.request.remote_addr)

		current_rating = query.get()

		if current_rating:
			template_values.update({'current_rating' :current_rating, 'current_stars' : int(current_rating.stars)})

		aggregate_query = StarReviewSummary.query(StarReviewSummary.movie_id == film_id)

		rating_summary = aggregate_query.get()
		logging.info(rating_summary)

		if rating_summary:
			template_values["ratings_summary"] = rating_summary
		template_values["ratings_summary_text"] = ratings.ratings_summary_text(template_values["ratings_summary"])


		self.response.out.write(template.render(template_values))

app = webapp2.WSGIApplication([
	webapp2.Route(r'/components/star-review/<film_id>', handler=StarReviewHandler),
	webapp2.Route(r'/components/bestandworstincinema/<quantity>', handler=BestAndWorstInCinema),
	],
	debug=True)