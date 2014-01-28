import urlparse
import urllib
import logging
import json
from google.appengine.api import memcache

from google.appengine.api.urlfetch import fetch

CONTENT_API_HOST = 'content.guardianapis.com'
SEARCH = 'search'
PARAMS = {'tag': 'film,tone/reviews',
          'show-fields': 'headline,thumbnail,trailText,star-rating',
          'show-tags': 'all',
          'date-id': 'date/last30days',
          'page': "1"}

def read_all(params=None):
    if not params:
        params = {}
        params.update(PARAMS)

    url = "http://%s/%s" % (CONTENT_API_HOST, SEARCH)
    if params:
        encoded_url = url + "?" + urllib.urlencode(params)

    result = fetch(encoded_url)
    logging.info('calling content api with %s' %encoded_url)
    if not result.status_code == 200:
        logging.warning("Content API read failed %d" % result.status_code)

    content = json.loads(result.content)
    if not 'response' in content:
        return None

    response = content['response']
    currentPage = response['currentPage']
    numPages = response['pages']
    results = response['results']

    while currentPage != numPages:
        params['page'] = str(1+int(currentPage))
        encoded_url = url + "?" + urllib.urlencode(params)
        result = fetch(encoded_url)
        logging.info(encoded_url)
        if not result.status_code == 200:
            logging.warning("Content API read failed %d" % result.status_code)
            return None
        content = json.loads(result.content)
        response = content['response']
        if not 'response' in content:
            logging.info('no response')
            return None
        currentPage = response['currentPage']
        logging.info(currentPage)
        results.extend(response['results'])
    results = [r for r in results if 'starRating' in r.get('fields', {}) and 'thumbnail' in r.get('fields', {})]
    return results

def read(content_id, params = None):

    url = "http://%s%s" % (CONTENT_API_HOST, content_id)

    if params:
        url = url + "?" + urllib.urlencode(params)

    cached_data = memcache.get(url)

    if cached_data:
        return cached_data

    result = fetch(url)

    if not result.status_code == 200:
        logging.warning("Content API read failed: %d" % result.status_code)
        return None

    memcache.set(url, result.content, time = 60 * 15)

    return result.content

def search(query):
    url = "http://content.guardianapis.com/search?%s" % urllib.urlencode(query)

    cached_data = memcache.get(url)

    if cached_data:
        return cached_data

    result = fetch(url)

    if not result.status_code == 200:
        logging.warning("Failed to search API: %s" % url)
        return None
    
    memcache.set(url, result.content, time=60*3)
    return result.content