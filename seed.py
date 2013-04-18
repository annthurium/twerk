##### This module makes Twitter api calls to add data into the database.

import model
from model import Tweet, User
from model import session
from datetime import datetime, date
import time

import twitter
from settings import AUTHENTICATED_API

from sqlalchemy import func

##### Global constants
MAX_REQUESTABLE_TWEETS = 200

##### Function definiions
def find_newest_tweet_id_in_DB(user_screen_name):
	"""Returns id of user's newest tweet in database"""
	
	# query for tweet with largest ID from user_name, since tweet IDs are sequential
	newest_tweet = session.query(func.max(Tweet.id)).filter_by(from_user_screen_name = user_screen_name).first()
	if newest_tweet is not None:
		return newest_tweet[0]
	else:
		return None

def get_tweets(user_screen_name):
	"""Calls functions add tweets into database, ensuring that there are no duplicates"""
	# find id of user's newest tweet in database
	newest_tweet_id = find_newest_tweet_id_in_DB(user_screen_name)

	if newest_tweet_id == None:
		newest_tweet_id = 0
	timeline = consume_timeline(user_screen_name, newest_tweet_id)
	if timeline:
		load_timeline(timeline)

def consume_timeline(user_name, newest_tweet_id):

	timeline = AUTHENTICATED_API.GetUserTimeline(screen_name = user_name, count=MAX_REQUESTABLE_TWEETS, 
		include_rts=True, since_id = newest_tweet_id)
	new_timeline_length = len(timeline)
	if new_timeline_length == 0:
		return
	max_id_returned = timeline[-1].id

	while new_timeline_length > 0:
		new_timeline = AUTHENTICATED_API.GetUserTimeline(screen_name = user_name, count=MAX_REQUESTABLE_TWEETS, 
		include_rts=True, since_id = newest_tweet_id, max_id = max_id_returned)

		# since max_id is inclusive, new_timeline[0] is a duplicate
		# so we throw it out:
		new_timeline.pop(0)
		new_timeline_length = len(new_timeline)
		if new_timeline_length == 0:
			break
		timeline.extend(new_timeline)
		max_id_returned = new_timeline[-1].id
	print "timeline length", len(timeline)
	print "last tweet returned", timeline[-1].text
	return timeline

def load_user(username):
	"""Adds user to database"""
	u = AUTHENTICATED_API.GetUser(username)
	new_user = User(id = u.id, screen_name = u.screen_name, 
		first_last_name = u.name, profile_img_url = u.profile_image_url)
	print "new_user", new_user.screen_name
	session.add(new_user)
	session.commit()

def load_timeline(timeline):
	"""Adds all tweets in timeline to database"""
	for item in timeline:
		timestamp = item.created_at
		from_user_sn = item.user.screen_name
		column_time = datetime.strptime(timestamp, "%a %b %d %H:%M:%S +0000 %Y")
		new_tweet = Tweet(id = item.id, from_user_id = item.user.id, text = item.text, 
			to_user_id = item.in_reply_to_user_id, to_user_screen_name = item.in_reply_to_screen_name,
			in_reply_to_status_id = item.in_reply_to_status_id, time_stamp = column_time, 
			from_user_screen_name = item.user.screen_name)

		session.add(new_tweet)
	session.commit()

def main():
	dictionary = AUTHENTICATED_API.GetRateLimitStatus()
	for k in dictionary:
		print k, dictionary[k]
	#user_name = ''
	#find_newest_tweet_id_in_DB(user_name)
	#get_tweets(user_name)
	# testing 2 tweets:
	#timeline = AUTHENTICATED_API.GetUserTimeline(screen_name = user_name, count=2, include_rts=True)

	#newest = find_newest_tweet_id_in_DB(user_name)

	#timeline = stripper.consume_timeline(user_name)
	#timeline = consume_timeline(user_name, 0)

if __name__ == "__main__":
	main()