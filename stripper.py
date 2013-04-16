import twitter
import string
from settings import AUTHENTICATED_API
# import en


MAX_REQUESTABLE_TWEETS = 200

def check_for_new_tweets_in_db():
	pass

def get_new_tweets():
	pass

def consume_timeline(user_name):
	# first request returns maximum allowable number of tweets
	# include_rts must be true in order to return the full number of results specified by count
	timeline = AUTHENTICATED_API.GetUserTimeline(screen_name = user_name, count=MAX_REQUESTABLE_TWEETS, include_rts=True)
	max_id_returned = timeline[-1].id
	new_timeline_length = len(timeline)

	# testing testing 1-2-3:
	# print "max_id = ", max_id_returned
	# print "text: ", timeline[-1].text
	# print "length:", len(timeline)

	while new_timeline_length != 0:
		new_timeline = AUTHENTICATED_API.GetUserTimeline(screen_name = user_name, count=MAX_REQUESTABLE_TWEETS, 
			include_rts=True, max_id = max_id_returned)

		# new_status[0] is a duplicate (equivalent to last tweet from previous request)
		# so we throw it out
		new_timeline.pop(0)

		new_timeline_length = len(new_timeline)
		print "new_timeline_length", new_timeline_length
		last_status_index = new_timeline_length - 1
		#print "last_status_index", last_status_index

		if new_timeline_length == 0:
			break

		timeline.extend(new_timeline)
		max_id_returned = new_timeline[last_status_index].id
		print "text: ", new_timeline[last_status_index].text
		#print "tweet_id", new_timeline[last_status_index].id

	print "len(timeline)", len(timeline)
	print timeline[-1].text
	return timeline

	# spot checking for duplicate tweets
	# for item in status:
	# 	if item.id==157891732237856768:
	# 		print item.text


def find_replies(user, timeline):
	f = open('data.txt', 'w')
	replies = []
	for tweet in timeline:
		if (tweet.in_reply_to_screen_name == user) or (string.find(tweet.text, user) != -1):
			f.write(tweet.text)
	#return replies

def build_relationship(user_1, user_2, timeline_1, timeline_2):
	find_replies(timeline_1, user_2)
	find_replies(timeline_2, user_1)

def main():
	
	user_1 = 'annthurium'
	user_2 = 'queerviolet'
	timeline_1 = consume_timeline(user_1)
	#timeline_2 = consume_timeline(user_2)
	#find_replies(user_2, timeline_1)
	# build_relationship(user_1, user_2, timeline_1, timeline_2)


	# new_list = []
	# for s in statuses:
	# 	if string.find(s.text, "@queerviolet") != -1:
	# 		new_list.append(s.text)
	# text = "".join(new_list)
	
	#summary = en.content.categorise(new_string)
	#for item in summary:
		#print item.name, item.count, item.type
if __name__ == "__main__":
	main()
