from flask import Flask
from redis import Redis, RedisError
import os
import socket

# Connect to Redis
redis = Redis(host="redis", db=0)

app = Flask(__name__)
try:  
   os.environ["TEST"]
except KeyError: 
   print ("Please set the environment variable TEST")
   sys.exit(1)

@app.route("/")
def hello():
    try:
        visits = redis.incr('counter')
    except RedisError:
        visits = "<i>cannot connect to Redis, counter disabled</i>"

    html = "<h3>Hello {name}!  {test}</h3>" \
           "<b>Hostname:</b> {hostname}<br/>" \
           "<b>Visits:</b> {visits}"
    return html.format(name=os.getenv('NAME', "world"), hostname=socket.gethostname(), visits=visits)


if __name__ == "__main__":
	app.run(host='0.0.0.0', port=80)
