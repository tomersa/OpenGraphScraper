1.  Description
   1. A web service that will scrape  Open graph tags. For any given URL.
   2. See http://ogp.me/ for definitions
   3. See https://developers.facebook.com/tools/debug/sharing/?q=http%3A%2F%2Fogp.me%2F for an example implementation
   4. The server provides the following JSON API 
      1. Request
         1. POST localhost:8080/stories?url={some_url}
      1. Response
         1. An ID representing the canonical URL of the given url (each canonical url should have a single matching id in the system) 

      1. Request
         1. GET localhost:8080/stories/{canoniacl-url-id}
      1. Response
         1. scrape_status field can be (done,error,pending)
         2. {
              "url": "http://ogp.me/",
              "type": "website",
              "title": "Open Graph protocol",
              "image": [
              {
                "url": "http://ogp.me/logo.png",
                "type": "image/png",
                "width": 300,
                "height": 300,
                "alt": "The Open Graph logo"
              },
              ],
              "updated_time": "2018-02-18T03:41:09+0000",
	      scrape_status: "done",
              "id": "10150237978467733"
          }
4. curl examples which demonstrate the usage of the service:
   curl -X POST --data "url=http://www.microsoft.com" localhost:8080/stories
   curl -X GET localhost:8080/stories/5c3db58c68002b1effb61a71
