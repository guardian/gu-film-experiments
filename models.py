from google.appengine.ext import ndb

class Configuration(ndb.Model):
	key = ndb.StringProperty()
	value = ndb.StringProperty()

class StarReview(ndb.Model):
	ip_address = ndb.StringProperty(required=True)
	stars = ndb.IntegerProperty(required=True)
	movie_id = ndb.StringProperty(required=True)

class StarReviewSummary(ndb.Model):
	movie_id = ndb.StringProperty(required=True)
	average_rating = ndb.IntegerProperty(required=True)
	max_rating = ndb.IntegerProperty(required=True)
	min_rating = ndb.IntegerProperty(required=True)
	ratings = ndb.IntegerProperty(required=True)