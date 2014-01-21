def pluralize(num):
	if num > 1:
		return 's'
	return ""

def ratings_summary_text(summary):
	if not summary or not hasattr(summary, "average_rating"):
		return "Rated 0 stars from 0 ratings"
	return "Rated {stars} star{star_suffix} from {ratings} rating{rating_suffix}".format(stars=summary.average_rating,
																						star_suffix=pluralize(summary.average_rating),
																						ratings=summary.ratings,
																						rating_suffix=pluralize(summary.ratings),
																						)