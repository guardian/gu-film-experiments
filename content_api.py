import urlparse
import urllib
import logging
import json
import datetime

from google.appengine.api import memcache

from google.appengine.api.urlfetch import fetch

import configuration

last_30_days = (datetime.date.today() + datetime.timedelta(days=-30)).isoformat()

CONTENT_API_HOST = configuration.lookup('CONTENT_API_HOST', 'content.guardianapis.com')
API_KEY = configuration.lookup('API_KEY')
SEARCH = 'search'
PARAMS = {
    'section' : 'film',
    'tag': 'tone/reviews',
    'show-fields': 'headline,thumbnail,trailText,star-rating',
    'show-tags': 'all',
    'from-date': last_30_days,
    'page': "1",
    }

if API_KEY:
    PARAMS['api-key'] = API_KEY

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
        #logging.info(encoded_url)
        if not result.status_code == 200:
            logging.warning("Content API read failed %d" % result.status_code)
            return results
        content = json.loads(result.content)
        response = content['response']
        if not 'response' in content:
            logging.info('no response')
            return results
        currentPage = response['currentPage']
        #logging.info(currentPage)
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
    url = "http://%s/search?%s" % (CONTENT_API_HOST, urllib.urlencode(query))

    cached_data = memcache.get(url)

    if cached_data:
        return cached_data

    result = fetch(url)

    if not result.status_code == 200:
        logging.warning("Failed to search API: %s" % url)
        return None
    
    memcache.set(url, result.content, time=60*3)
    return result.content