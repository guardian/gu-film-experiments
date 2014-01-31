import os
import json
import jinja2
import webapp2
import film_reviews
import logging
import random
import ratings
import headers
import content_api

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

		headers.cors(self.response)
		self.response.out.write(template.render(template_values))

class ReviewsByGenreHandler(webapp2.RequestHandler):
	def get(self):
		template = jinja_environment.get_template('reviews-by-genre.html')

		params = { 
			'section' : 'film',
			'page-size' : '50',
			'show-fields' : 'headline,thumbnail,byline,starRating',
		}

		def trails_from_results(content):
			if not content:
				return []

			data = json.loads(content)
			results =  data.get("response", {}).get("results", [])

			random.shuffle(results)

			return [r for r in results if "thumbnail" in r["fields"]][:3]



		template_values = {
		}

		def grab_reviews(genre_tag):
			search_params = {
				'tag' : "tone/reviews,%s" % genre_tag,
			}
			search_params.update(params)
			return trails_from_results(content_api.search(search_params))

		template_values['reviews'] =[
			{
				"heading" : "Drama",
				"reviews" : grab_reviews("film/drama"),
				"tag_name" : "film/drama",
			},
			{
				"heading" : "Comedy",
				"reviews" : grab_reviews("film/comedy"),
				"tag_name" : "film/comedy",
			},
			{
				"heading" : "Science fiction",
				"reviews" : grab_reviews("film/sciencefictionandfantasy"),
				"tag_name" : "film/sciencefictionandfantasy",
			},]

		headers.cors(self.response)
		self.response.out.write(template.render(template_values))

app = webapp2.WSGIApplication([
	webapp2.Route(r'/components/star-review/<film_id>', handler=StarReviewHandler),
	webapp2.Route(r'/components/bestandworstincinema/<quantity>', handler=BestAndWorstInCinema),
	webapp2.Route(r'/components/front/genre-reviews', handler=ReviewsByGenreHandler),
	],
	debug=True)