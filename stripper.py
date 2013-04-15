import twitter
import string
from settings import AUTHENTICATED_API
# import en

USER_NAME = 'annthurium' #obvs this will change later
MAX_REQUESTABLE_TWEETS = 200

def consume_timeline():
	# first request returns maximum allowable number of tweets
	# include_rts must be true in order to return the full number of results specified by count
	status = AUTHENTICATED_API.GetUserTimeline(screen_name=USER_NAME, count=200, include_rts=True)
	max_id_returned = status[-1].id
	print "max_id = ", max_id_returned
	print "text: ", status[-1].text
	print "length:", len(status)

	# Does it make my code run more slowly to define a function inside a function? Should this live somewhere else?
	def get_page(max_id_returned, status_length):
		while status_length != 0:
			new_status = AUTHENTICATED_API.GetUserTimeline(screen_name=USER_NAME, count=MAX_REQUESTABLE_TWEETS, 
				include_rts=True, max_id = max_id_returned)

			# new_status[0] is a duplicate (equivalent to last tweet from previous request)
			# so we throw it out
			new_status.pop(0)

			status_length = len(new_status)
			print "status_length", status_length
			last_status_index = status_length - 1
			print "last_status_index", last_status_index

			if status_length == 0:
				return

			status.extend(new_status)
			max_id_returned = new_status[last_status_index].id
			print "text: ", new_status[last_status_index].text
			print "tweet_id", new_status[last_status_index].id
			print "len status", len(status)

	get_page(max_id_returned, len(status))

	# spot checking for duplicate tweets
	# for item in status:
	# 	if item.id==157891732237856768:
	# 		print item.text

def main():
	consume_timeline()
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
