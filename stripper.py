import twitter
import string
from settings import AUTHENTICATED_API
#import en

# I know global variables are bad, is there a better way to do this?

USER_NAME = 'annthurium' #obvs this will change later
MAX_REQUESTABLE_TWEETS = 200

def consume_timeline():
	# first request returns maximum allowable number of tweets
	# include_rts must be true in order to return the full number of results specified by count
	status = AUTHENTICATED_API.GetUserTimeline(screen_name=USER_NAME, count=100, include_rts=True)
	max_id_returned = status[-1].id
	print "max_id = ", max_id_returned
	print "text: ", status[-1].text
	print "length:", len(status)
	def get_page(max_id_returned):
		new_status = api.GetUserTimeline(screen_name=USER_NAME, count=MAX_REQUESTABLE_TWEETS, include_rts=True, max_id = max_id_returned)
		# new_status[0] is a duplicate (equivalent to last tweet from previous request)
		# so we throw it out
		new_status.pop(0)
		status.extend(new_status)
		max_id_returned_2 = new_status[-1].id
		print "text: ", new_status[-1].text
		print "tweet_id", new_status[-1].id
		print "len new_status", len(new_status)
		print "len status", len(status)
		# with len(new_status) < 196, it returns 2882 results.
		# with len(new_status) >= 196, I get 1687 results
		# I am confuse
		if len(new_status) < 196:
			return len(new_status)
		else:
			get_page(max_id_returned_2)
	#get_page(max_id_returned)

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
