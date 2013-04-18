##### Views for WSGI application live here. 
##### (Wait, what? WSGI? Oooh, FANCY terminology there, captain.)
##### Shut your piehole you.

from flask import Flask, render_template, redirect, request, url_for, flash, session, g
from model import session as db_session, User, Tweet
import model
import stripper

app = Flask(__name__)
SECRET_KEY = "dumbass_horse_battery_staple_FOREVAR_AND_EVAR"

@app.teardown_request
def shutdown_session(exception = None):
    db_session.remove()

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/list_tweets", methods=["POST", "GET"])
def list_tweets():
    user_1_screen_name = request.form['user_1_screen_name']
    user_2_screen_name = request.form['user_2_screen_name']
    print user_2_screen_name
    print user_1_screen_name
    tweet_list_1 = query_for_tweets(user_1_screen_name, user_2_screen_name)
    tweet_list_2 = query_for_tweets(user_2_screen_name, user_1_screen_name)
    return render_template("list_tweets.html", tweet_list = tweet_list_1)

def query_for_tweets(user_1_screen_name, user_2_screen_name):
	search_string = "%@" + user_2_screen_name + "%"
	tweet_list = model.session.query(Tweet).filter(Tweet.text.like(search_string)).filter(Tweet.from_user_screen_name == user_1_screen_name)
	return tweet_list

if __name__== "__main__":
	app.run(debug = True)