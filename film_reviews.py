import logging
from google.appengine.api import memcache
import content_api

def filtered_reviews(max_or_min=None,star_value=None):
    logging.info(star_value)
    min = max_or_min == 'min'
    if min:
        star_query = "reviews_gte_%s" % str(star_value)
    else:
        star_query = 'reviews_lte_%s' % str(star_value)

    filtered_reviews = memcache.get(star_query)

    if not filtered_reviews:
        logging.info("memcache doesn't have query %s " % star_query)
        all_reviews = memcache.get('data_reviews')
        if not all_reviews:
            logging.info('memcache is empty - calling the content api')
            all_reviews = content_api.read_all()
            memcache.set('data_reviews', all_reviews, 15*60)
        if min:
            logging.info('calling the min function')
            filtered_reviews = [r for r in all_reviews if r['fields']['starRating'] >= star_value]
            filtered_reviews = sorted(filtered_reviews,key=lambda x:x['webPublicationDate'], reverse=True)
            filtered_reviews = sorted(filtered_reviews,key=lambda x:x['fields']['starRating'], reverse=True)
        else:
            filtered_reviews = [r for r in all_reviews if r['fields']['starRating'] <= star_value]
            filtered_reviews = sorted(filtered_reviews,key=lambda x:x['webPublicationDate'], reverse=True)
            filtered_reviews = sorted(filtered_reviews,key=lambda x:x['fields']['starRating'])
        memcache.set(star_query, filtered_reviews, 15*60)
    return filtered_reviews