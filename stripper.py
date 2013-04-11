import twitter
import string
import en


def main():
	api = twitter.Api(consumer_key='jfSslPak6IKaQkKDa0KQ',
                      consumer_secret='imTaptYqLhtUFYpsk6NAZP5NNftayqpup6ZyFY7Xbb8',
                      access_token_key='17101287-E1M6GPPSKTHAcE4fVWSB8AiVB1FGB0ahKlXkndJvc',
                      access_token_secret='UoW1TTIi73alCrRhwa3ecFnWukcnXP0Qiam7pTSuYU')

	statuses = api.GetUserTimeline(screen_name='annthurium', count=50)
	#print [s.text for s in statuses]
	new_list = []
	for s in statuses:
		if string.find(s.text, "@queerviolet") != -1:
			new_list.append(s.text)
	text = "".join(new_list)
	print text
	#summary = en.content.categorise(new_string)
	#for item in summary:
		#print item.name, item.count, item.type
if __name__ == "__main__":
	main()
