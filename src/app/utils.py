from flask import make_response
from opengraph import OpenGraph
from pymongo import MongoClient
from threading import Thread
JSON_MIME_TYPE = 'application/json'

db_name = 'urls_db'

# ~~ statuses ~~
PENDING_STATUS = 0
DONE_STATUS = 1
ERROR_STATUS = 2

STATUSES = {PENDING_STATUS : 'pending', DONE_STATUS: 'done', ERROR_STATUS: 'error'}

def json_response(data='', status=200, headers=None):
    headers = headers or {}
    if 'Content-Type' not in headers:
        headers['Content-Type'] = JSON_MIME_TYPE

    return make_response(data, status, headers)


def get_canonical_url(u):
    u = u.lower()
    if u.startswith("http://"):
        u = u[7:]
    if u.startswith("www."):
        u = u[4:]
    if u.endswith("/"):
        u = u[:-1]
    return u


def og_scrape_worker(canonical_url):
    # Get open graph data
    try:
        og_data = OpenGraph(url="http://%s" % canonical_url)
        if og_data.is_valid():
            return add_data_to_url_in_db(canonical_url, og_data)
        else:
            update_to_error_url_status_in_db(canonical_url)

    except Exception as e:
        update_to_error_url_status_in_db(canonical_url)


def scrape_url(canonical_url):
    id = create_pending_url_in_db(canonical_url)

    og_thread = Thread(target=og_scrape_worker, args=(canonical_url,))
    og_thread.start()
    return id


# ~~ Database operations ~~
def get_url_id_from_db(url):
    urls_collection = get_urls_collection()
    url_doc = urls_collection.find_one({"url": url})

    return None if not url_doc else url_doc['_id']


def is_error(url_id):
    urls_collection = get_urls_collection()
    url_doc = urls_collection.find_one({"_id": url_id})

    return False if not url_doc else url_doc['status'] == ERROR_STATUS


def get_urls_database():
    client = MongoClient()
    return client[db_name]


def get_urls_collection():
    return get_urls_database()['urls']


def get_og_collection():
    return get_urls_database()['open_graph']


def create_pending_url_in_db(url):
    urls_collection = get_urls_collection()

    doc = {'url': url, 'status': PENDING_STATUS}
    id = urls_collection.insert_one(doc).inserted_id

    return id


def add_data_to_url_in_db(url, og_data): # Assuming data coming from the open graph will have the 'url' attribute with the url
    og_collection = get_og_collection()
    og_data_id = og_collection.insert_one(og_data).inserted_id

    urls_collection = get_urls_collection()
    url_doc = urls_collection.find_one({'url': url})
    url_doc['status'] = DONE_STATUS
    url_doc['data_id'] = og_data_id

    urls_collection.update_one(filter={'url': url}, update={'$set': url_doc})

    return url_doc['_id']


def update_to_error_url_status_in_db(url):
    urls_collection = get_urls_collection()
    url_doc = urls_collection.find_one({'url': url})
    url_doc['status'] = ERROR_STATUS

    urls_collection.update_one(filter={'url': url}, update={'$set':url_doc})


def get_url_data_from_db(url_id): # Assuming data coming from the open graph will have the 'url' attribute with the url
    og_collection = get_og_collection()
    urls_collection = get_urls_collection()

    url_doc = urls_collection.find_one({'_id': url_id})
    status = url_doc['status']
    out = {} if status != DONE_STATUS else og_collection.find_one({'_id': url_doc['data_id']})
    out['scrape_status'] = STATUSES[status]
    del out['_id']

    return out