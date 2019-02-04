============= Intro ============= 
This service uses Open Graph to scrape tags from any given url
See http://ogp.me/ for definitions

============= API ============= 
The server provides the following JSON API 
Request:  POST localhost:8080/stories?url={some_url}
Response: ID representing the canonical URL of the given url (each canonical url should have a single matching id in the system) 

Request:  GET localhost:8080/stories/{canonical-url-id}
Response: JSON:
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
	      scrape_status: "done", //can be (done,error or pending)
              "id": "10150237978467733"
          }

============= Tech stack ============= 
Flask
Python
OpenGraph python library.
*For more information check out the requirements.txt

============= example curl commands ============= 
curl examples which demonstrate the usage of the service:
curl -X POST --data "url=http://www.microsoft.com" localhost:8080/stories
curl -X GET localhost:8080/stories/5c3db58c68002b1effb61a71
*Assuming 5c3db58c68002b1effb61a71 is the id returned from the post command

