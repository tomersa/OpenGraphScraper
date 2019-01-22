from flask import Flask, request
from .utils import *
from bson.objectid import ObjectId

app = Flask(__name__)


@app.route('/stories', methods=['POST'])
def stories_post():
    # 1st request
    if request.method == 'POST':
        url = request.form['url']
        canonical_url = get_canonical_url(url)
        canonical_url_id = get_url_id_from_db(canonical_url)

        if not canonical_url_id or is_error(canonical_url_id):
            canonical_url_id = scrape_url(canonical_url)

        return "%s" % canonical_url_id, 200, {'Content-Type': JSON_MIME_TYPE}


@app.route('/stories/<string:url_id>', methods=['GET'])
def stories_get(url_id):
    # 2nd request
    if request.method == 'GET':
        return "%s" % get_url_data_from_db(ObjectId(url_id)), 200, {'Content-Type': JSON_MIME_TYPE}

# 1st request
#       1. Request
#          1. POST localhost:8080/stories?url={some_url}
#       1. Response
#          1. An ID representing the canonical URL of the given url (each canonical url should have a single matching id in the system)
# 2nd request
#       1. Request
#          1. GET localhost:8080/stories/{canoniacl-url-id}
#       1. Response
#          1. scrape_status field can be (done,error,pending)
#          2. {
#               "url": "http://ogp.me/",
#               "type": "website",
#               "title": "Open Graph protocol",
#               "image": [
#               {
#                 "url": "http://ogp.me/logo.png",
#                 "type": "image/png",
#                 "width": 300,
#                 "height": 300,
#                 "alt": "The Open Graph logo"
#               },
#               ],
#               "updated_time": "2018-02-18T03:41:09+0000",
# 	      scrape_status: "done",
#               "id": "10150237978467733"
#           }
