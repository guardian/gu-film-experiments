#consume the data feed
#shuffle
#restrict to x
#render html
import os
import jinja2
import webapp2
import film_reviews
import logging
import random

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), "templates")))

class BestAndWorstInCinema(webapp2.RequestHandler):
    def get(self, quantity):
        five_star = film_reviews.filtered_reviews('min', '5')
        one_star = film_reviews.filtered_reviews('max', '1')
        template = jinja_environment.get_template('bestandworstincinema.html')
        reviews = []
        map(random.shuffle, [five_star, one_star])
        reviews.extend(five_star[:int(quantity)])
        reviews.extend(one_star[:int(quantity)])

        self.response.out.write(template.render({'reviews':reviews}))
