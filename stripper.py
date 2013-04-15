import twitter
import string
from settings import AUTHENTICATED_API
# import en


MAX_REQUESTABLE_TWEETS = 200

# why is this function not reaching the end of the timeline? I'm confused. Sigh.
def consume_timeline(user_name):
	# first request returns maximum allowable number of tweets
	# include_rts must be true in order to return the full number of results specified by count
	timeline = AUTHENTICATED_API.GetUserTimeline(screen_name = user_name, count=200, include_rts=True)
	max_id_returned = timeline[-1].id
	#print "max_id = ", max_id_returned
	#print "text: ", timeline[-1].text
	#print "length:", len(timeline)

	# Does it make my code run more slowly to define a function inside a function? Should this live somewhere else?
	def get_page(max_id_returned, timeline_length):

		while timeline_length != 0:
			new_timeline = AUTHENTICATED_API.GetUserTimeline(screen_name = user_name, count=MAX_REQUESTABLE_TWEETS, 
				include_rts=True, max_id = max_id_returned)

			# new_status[0] is a duplicate (equivalent to last tweet from previous request)
			# so we throw it out
			new_timeline.pop(0)

			new_timeline_length = len(new_timeline)
			#print "new_timeline_length", new_timeline_length
			last_status_index = new_timeline_length - 1
			#print "last_status_index", last_status_index

			if new_timeline_length == 0:
				return

			timeline.extend(new_timeline)
			max_id_returned = new_timeline[last_status_index].id
			#print "text: ", new_timeline[last_status_index].text
			#print "tweet_id", new_timeline[last_status_index].id

	get_page(max_id_returned, len(timeline))
	print "len(timeline)", len(timeline)
	return timeline

	# spot checking for duplicate tweets
	# for item in status:
	# 	if item.id==157891732237856768:
	# 		print item.text

#def consume

def find_replies(timeline, user):
	replies = []
	for tweet in timeline:
		if (tweet.in_reply_to_screen_name == user) or (string.find(tweet.text, user) != -1):
			replies.append(tweet.text)
	print replies[-1]
	return replies

def build_relationship(user_1, user_2, timeline_1, timeline_2):
	find_replies(timeline_1, user_2)
	find_replies(timeline_2, user_1)

def main():
	pass
	rate_limit = AUTHENTICATED_API.GetRateLimitStatus()
	for k in rate_limit:
		print k, rate_limit[k]
	# user_1 = 'annthurium'
	# user_2 = 'queerviolet'
	# timeline_1 = consume_timeline(user_1)
	# timeline_2 = consume_timeline(user_2)
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
