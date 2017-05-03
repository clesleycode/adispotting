import requests
import time

urls = [ # this is a list of urls that you want to ping. Feel free to add more than one.
  "https://salty-stream-23282.herokuapp.com/",
  ]

while True:
    for url in urls:
        requests.get(url) # pinging the server
        time.sleep(300) 
