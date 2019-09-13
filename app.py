import flask
import random
import os
import requests
import json

app = flask.Flask(__name__)

url = "https://api.genius.com/search?q=Drake"
artisturl = "https://genius.com/artists/Drake"
    
my_header = {
    "Authorization": os.getenv("Authorization")
}

oauth = requests.OAuthHandler(
    os.getenv("APIKEY"),
    os.getenv("APISECRET")
    )
oauth.set_access_token(
    os.getenv("ACCESSTOKEN"),
    os.getenv("ACCESSKEY")
    ) 
    
api = requests.API(oauth)
response = requests.get(url, headers=my_header)

def Randomized():
    bio = response.json()
    top_songs = bio["response"]["popular"]
    ranint = random.randint(0,len(top_songs)-1)
    song = top_songs[ranint]
    return song


def getTweets():
    tweets = set()
    searching = api.search("@Drake")
    for tweets in range(0,12):
        tweets.add(random.choice(searching).text)
    return list(tweets)
    
def getImage(song):
    im = song["result"]["header_image_url"]
    return im

def getSong(song):
    sn = song["result"]["title"]
    return sn

@app.route('/')
def result(): 
    song = Randomized()
    return flask.render_template("Layout.html",im = getImage(song),
    tweets = getTweets(),artisturl = "https://genius.com/artists/Drake",song_name = getSong(song))
    
app.run(
    port = int(os.getenv('PORT',8080)),
    host = os.getenv('IP', '0.0.0.0')
    )