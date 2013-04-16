from flask import Flask, render_template, redirect, request, url_for, flash, session, g
from model import session as db_session, User, Tweet
import model
import stripper

app = Flask(__name__)
SECRET_KEY = "dumbass_horse_battery_staple_FOREVAR_AND_EVAR"

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/list_tweets")
def list_tweets():
	tweet_list = model.session.query(Tweet).filter(Tweet.text.like("%@queerviolet%"))
	return render_template("list_tweets.html", tweet_list = tweet_list)

#list = session.query(Tweet).filter(Tweet.text.like("%@queerviolet%"))

#def something():
	#pass
	#user_1 = 'annthurium'
	#user_2 = 'queerviolet'
	# timeline_1 = stripper.consume_timeline(user_1)
	# timeline_2 = stripper.consume_timeline(user_2)
	# replies = stripper.find_replies(timeline_1, user_2)
	# moar_replies = stripper.find_replies(timeline_2, user_1)
	# return render_template("list_tweets.html", at_replies = replies)

if __name__== "__main__":
	app.run(debug = True)