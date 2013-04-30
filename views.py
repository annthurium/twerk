##### Flask views live here (in all their glory.)

from flask import Flask, render_template, redirect, request, url_for, flash, session, g
from model import session as db_session, User, Tweet
from sqlalchemy import or_
import model
import seed
import en
import calendar
from datetime import datetime

app = Flask(__name__)
app.secret_key = "dumbass_horse_battery_staple_FOREVAR_AND_EVAR"

@app.teardown_request
def shutdown_session(exception = None):
    db_session.remove()

##### Route functions #####

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/streamgraph_sample")
def streamgraph_sample():
    return render_template("streamgraph_sample.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

# Easter egg
@app.route("/georgia_okeefe")
def georgia_okeefe():
    return render_template("georgia_okeefe.html")

@app.route("/list_tweets", methods=["POST", "GET"])
def list_tweets():
    user_1_screen_name = strip_leading_ampersand(str(request.form['user_1_screen_name']))
    user_2_screen_name = strip_leading_ampersand(str(request.form['user_2_screen_name']))
    # check to see if this data already exists in session
    # if not, send them back to the index page to enter their data
    seed.get_tweets(user_1_screen_name)
    seed.get_tweets(user_2_screen_name)
    tweet_list_1 = query_for_tweets(user_1_screen_name, user_2_screen_name)
    tweet_list_2 = query_for_tweets(user_2_screen_name, user_1_screen_name)
    session['user_1_screen_name'] = user_1_screen_name
    session['user_2_screen_name'] = user_2_screen_name
    return render_template("list_tweets.html", 
                            tweet_list_1 = tweet_list_1, 
                            tweet_list_2 = tweet_list_2,
                            user_1 = user_1_screen_name, 
                            user_2 = user_2_screen_name)

@app.route("/analysis")
def analysis():
    tweet_list_1 = query_for_tweets(session['user_1_screen_name'], session['user_2_screen_name'])
    tweet_list_2 = query_for_tweets(session['user_2_screen_name'], session['user_1_screen_name'])
    summary_1 = rid_analyze(tweet_list_1)
    summary_2 = rid_analyze(tweet_list_2)
    return render_template("analysis.html", 
                            rid_summary_1=summary_1,
                            rid_summary_2=summary_2,
                            user_1 = session['user_1_screen_name'],
                            user_2 = session['user_2_screen_name'])


@app.route("/graph")
def make_graph():
    tweet_list_1 = query_for_tweets(session['user_1_screen_name'], session['user_2_screen_name'])
    #tweet_list_2 = query_for_tweets(session['user_2_screen_name'], session['user_1_screen_name'])
    list_1_len = count_list_of_tweets(tweet_list_1)

    NUM_POINTS = 10

    # list_1_len will need to be rounded so as to ensure same number of points but I'll worry about that later
    n = list_1_len / NUM_POINTS

    tweet_text_1 = make_sub_list(tweet_list_1, NUM_POINTS, list_1_len)


    primary = []
    secondary = []
    emotions = []

    # break list of tweets up into sub lists

    for count, item in enumerate(tweet_list_1):
        new_list

    # run rid analysis on sub list

    keys = ['primary', 'secondary', 'emotions']
    dictionary = dict.fromkeys(keys, 0)
    # Data for graph lives in NESTED DICTIONARIES. 
    # KEY is primary/secondary/emotions, 
    # values are a list of dictionaries (x is key, y is value)(x is key, y is value)


##### Helper functions #####

def make_sub_list(list_of_tweets, n, list_length):
    """Divides list of tweets into length of size n.
    Returns concatented text from list of tweets"""
    return [cat_list_of_tweets(list_of_tweets[i:i + n]) for i in range(0, list_length, n)]

def count_list_of_tweets(list_of_tweets):
    """ Seems like there should be a better way to do this but I couldn't find one."""
    count = 0
    for item in list_of_tweets:
        count += 1
    return count

def strip_leading_ampersand(string):
    """Exactly what it says on the tin"""
    if string[0] == '@':
        new_string = string[1:]
        return new_string
    return string

def rid_analyze(tweet_list):
    """Performs psychological content analysis using regressive imagery dictionary.
    Returns sorted list of categories found in a text."""

    tweet_text = cat_list_of_tweets(tweet_list)
    summary = en.content.categorise(tweet_text)
    return summary

def cat_list_of_tweets(tweet_list):
    """Concatenates list of strings into one big string."""
    return ''.join([item.text for item in tweet_list])

def query_for_tweets(user_1_screen_name, user_2_screen_name):
    """Queries database for @replies and mentions of user_2 in user_1 tweet stream."""
    search_string = "%@" + user_2_screen_name + "%"
    tweet_list = model.session.query(Tweet).filter(or_(Tweet.text.like(search_string), Tweet.to_user_screen_name==user_2_screen_name)).filter(Tweet.from_user_screen_name == user_1_screen_name)
    return tweet_list

if __name__== "__main__":
	app.run(debug = True)