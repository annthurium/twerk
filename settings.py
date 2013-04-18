import twitter
import os

twerkit_baby_api = twitter.Api(consumer_key=os.environ['consumer_key'],
                      consumer_secret=os.environ['consumer_secret'],
                      access_token_key=os.environ['access_token_key']
                      access_token_secret=os.environ['access_token_secret'])

AUTHENTICATED_API = twerkit_baby_api