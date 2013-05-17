##### Flask views live here (in all their glory.)

from flask import Flask, render_template, redirect, request, url_for, flash, session, g, jsonify
from model import session as db_session, User, Tweet
from sqlalchemy import or_
from flask_heroku import Heroku
import os
import model
import seed
import en
import itertools
import json

# for graphing date and time
import collections
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = "dumbass_horse_battery_staple_FOREVAR_AND_EVAR"

# do I need this code? Hmm.
app.config.from_object(__name__)

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

# Creating classes of named tuple
ScoreKey = collections.namedtuple('Score', ['name', 'type'])
AnalyzedTweet = collections.namedtuple('AnalyzedTweet', ['ts', 'id', 'summary', 'text', 'from_user'])
LayerKey = collections.namedtuple('LayerKey', ['from_user', 'name', 'type'])
Point = collections.namedtuple('Point', ['x', 'y'])

@app.route("/graph")
def make_graph():
    user_1_screen_name = strip_leading_ampersand(request.args.get('user_1_screen_name'))
    user_2_screen_name = strip_leading_ampersand(request.args.get('user_2_screen_name'))
    # check to see if this data already exists in session
    # if not, send them back to the index page to enter their data
    seed.get_tweets(user_1_screen_name)
    seed.get_tweets(user_2_screen_name)

    tweet_list_1 = query_for_tweets(user_1_screen_name, user_2_screen_name)
    tweet_list_2 = query_for_tweets(user_2_screen_name, user_1_screen_name)

    tweet_analyses = []

    layers = {}
    for tweet in itertools.chain(tweet_list_1, tweet_list_2):
        summary = en.content.categorise(tweet.text)
        all_summaries = {}
        for item in summary:
            all_summaries[ScoreKey(name = item.name, 
                                   type = item.type)] = item.count
            layers[LayerKey(from_user=tweet.from_user_screen_name, name=item.name, type=item.type)] = []
        tweet_analyses.append(AnalyzedTweet(ts = tweet.time_stamp,
                                            id = tweet.id,
                                            summary = all_summaries,
                                            text = tweet.text,
                                            from_user = tweet.from_user_screen_name))

    sorted_tweets = sorted(tweet_analyses, key=lambda x:x.ts)
    for tweet in sorted_tweets:
        for key in layers:
            try:
                layers[key].append(tweet.summary[ScoreKey(key.name, key.type)])
            except KeyError:
                layers[key].append(0)
    #sorted_layers = sorted(layers.keys(), key=lambda k:sum(layers[k]))

    json_layers = []
    for layer in layers:
        json_layers.append({'name': '%s: %s, %s' %
            (layer.from_user,
             layer.type, layer.name),
                            'username': layer.from_user,                            
                            'values': [{'x': x, 'y': y} for x, y in enumerate(layers[layer])]})
    return render_template("graph.html", 
        data=json.dumps(json_layers),
        tweet_list = sorted_tweets,
        user1=user_1_screen_name,
        user2=user_2_screen_name,
        num_tweets=len(sorted_tweets))


# def old_make_graph():
#     tweet_list_1 = query_for_tweets(session['user_1_screen_name'], session['user_2_screen_name'])
#     tweet_list_2 = query_for_tweets(session['user_2_screen_name'], session['user_1_screen_name'])
#     list_1_len = count_list_of_tweets(tweet_list_1)

#     # find earliest tweet in either list
#     # this code assumes tweets are ordered from least recent to most recent
#     # and they should be, because the database orders tweets sequentially by id number
#     list_1_start_date = tweet_list_1[0].time_stamp
#     list_2_start_date = tweet_list_2[0].time_stamp

#     earliest_date = min(list_1_start_date, list_2_start_date)

#     # find latest tweet in either list
#     list_1_end_date = tweet_list_2[-1].time_stamp
#     list_2_end_date = tweet_list_2[-1].time_stamp

#     latest_date = max(list_1_end_date, list_2_end_date)


#     def tweets_by_month(tweets):
#         month = None
#         batch = []
#         for tweet in tweets:
#             if month != tweet.time_stamp.month:
#                 if batch: # if batch is not empty
#                     yield batch
#                 month = tweet.time_stamp.month
#                 batch = []
#             batch.append(tweet)

#     for batch in tweets_by_month(tweet_list_1):
#         for tweet in batch:
#             print tweet.time_stamp
#         print "\n"

#     return
    # month_year_list = []
    # months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
    # start_year = earliest_date.year
    # end_year = latest_date.year
    # year_range = range(start_year, end_year+1)
    # for year in year_range:
    #     for month in months:
    #         d_string = str(year) + "-" + month
    #         month_year_list.append(d_string)


    # # should I be using dictionaries for this?
    # # this should probably just be a list
    # # or should I write some kind of container class? Decisions decisions
    # tweets_over_time = dict.fromkeys(month_year_list, 0)

    #  fmt = '%Y-%m' # This will make sorting easier, I think?

    # start_month = earliest_date.month
    # start_year = earliest_date.year
    # for item tweet_list_1:
    #     d_string = item.time_stamp.strftime(fmt)
    #     if tweets_over_time[d_string] == 0:
    #         tweets_over_time[d_string] = item.text
    #     else:
    #         # this seems horribly inefficient, there must be a better way
    #         tweets_over_time[d_string = new_dictionary[d_string] + " " + item.text
        
    # # so now we have a dict of date value, tweet text
    # for key in tweets_over_time:
    #     if tweets_over_time[key] != 0:
    #         tweets_over_time[key] = en.content.categorise(tweets_over_time[key])

    # # now we have a dictionary of month:RID score items

    # # compressing data in dictionary to make graphing easier
    # # I'll modify this later to make a fancier graph

    # for key in tweets_over_time:
    #     primary = 0
    #     secondary = 0
    #     emotions = 0
    #     if tweets_over_time[key] != 0:
    #         for item in tweets_over_time[key]:
    #             if item.type == "emotions":
    #                 emotions += item.count
    #             elif item.type == "secondary":
    #                 secondary += item.count
    #             else:
    #                 primary += item.count
    #     nested_dictionary = {'primary':primary, 'secondary':secondary, 'emotions':emotions}
    #     tweets_over_time[key] = nested_dictionary
    # # now we have a dictionary of month:{primary:count, secondary:count, emotions:count}

    # # come time to sort the dict
    # ordered_tweets_over_time = collections.OrderedDict(sorted(ordered_tweets_over_time.items()))

    # num_months = len(month_year_list)

    # # I don't actually need a dictionary
    # # flask jsonify extension takes named parameters

    # primary = []
    # secondary = []
    # emo = []
    # x = 0
    # for key in ordered_tweets_over_time:
    #     primary.append({'x': x, 'y': ordered_tweets_over_time[key]['primary']})
    #     secondary.append({'x': x, 'y': ordered_tweets_over_time[key]['secondary']})
    #     emo.append({'x': x, 'y': ordered_tweets_over_time[key]['emotions']})
    #     x += 1
    # layers = [
    #   {'name': 'primary', 'values': primary},
    #   {'name': 'secondary', 'values': secondary},
    #   {'name': 'emotional', 'values': emo}
    # ]

    # # now we have to sort it again, because dictionaries. Sigh.


    # # sorting second layer:
    # for val in layers:
    #     for key in val:
    #         val[key] = collections.OrderedDict(sorted(val.items()))



    # # This is doing it the bucket way
    # # NUM_POINTS = 10
    # # # list_1_len will need to be rounded so as to ensure same number of points but I'll worry about that later
    # # n = list_1_len / NUM_POINTS

    # # #tweet_text_1 = make_sub_list(tweet_list_1, NUM_POINTS, list_1_len)


    # primary = []
    # secondary = []
    # emotions = []

    # # break list of tweets up into sub lists

    # for count, item in enumerate(tweet_list_1):
    #     new_list

    # # run rid analysis on sub list

    # keys = ['primary', 'secondary', 'emotions']
    # dictionary = dict.fromkeys(keys, 0)
    # # Data for graph lives in NESTED DICTIONARIES. 
    # # KEY is primary/secondary/emotions, 
    # values are a list of dictionaries (x is key, y is value)(x is key, y is value)


##### Helper functions #####


# ##### These are for the "bucket" method of showing tweets over time.
# def make_sub_list(list_of_tweets, n, list_length):
#     """Divides list of tweets into length of size n.
#     Returns concatented text from list of tweets"""
#     return [cat_list_of_tweets(list_of_tweets[i:i + n]) for i in range(0, list_length, n)]

# def count_list_of_tweets(list_of_tweets):
#     """ Seems like there should be a better way to do this but I couldn't find one."""
#     count = 0
#     for item in list_of_tweets:
#         count += 1
#     return count



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
    db_uri = app.config.get('SQLALCHEMY_DATABASE_URI')
    if not db_uri:
        db_uri = "sqlite:///twerk.db"
    model.connect(db_uri)
    app.run(debug=True, port=int(os.environ.get("PORT", 5000)), host = "0.0.0.0")