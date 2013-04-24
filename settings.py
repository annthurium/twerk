import twitter
import os

shippit_api = twitter.Api(consumer_key='jfSslPak6IKaQkKDa0KQ',
                      consumer_secret='imTaptYqLhtUFYpsk6NAZP5NNftayqpup6ZyFY7Xbb8',
                      access_token_key='17101287-E1M6GPPSKTHAcE4fVWSB8AiVB1FGB0ahKlXkndJvc',
                      access_token_secret='UoW1TTIi73alCrRhwa3ecFnWukcnXP0Qiam7pTSuYU')

twerkit_baby_api = twitter.Api(consumer_key='8W5I3y8Y26SC6i0tzA8VCw',
                      consumer_secret='OxyDU41nts2D2rjjoJQw0doa9TzJ9QFOto49XUORM',
                      access_token_key='17101287-iaaStWKzjgdWxLcv8hMD8nhHfNAKB1dBfVv40wtXi',
                      access_token_secret='Ffdh2gY55mhyQsr1qMy859qiD3nfQyr0llSQTMKI')

AUTHENTICATED_API = twerkit_baby_api

#heroku config:set consumer_key=8W5I3y8Y26SC6i0tzA8VCw consumer_secret=OxyDU41nts2D2rjjoJQw0doa9TzJ9QFOto49XUORM access_token_key=17101287-iaaStWKzjgdWxLcv8hMD8nhHfNAKB1dBfVv40wtXi access_token_secret=Ffdh2gY55mhyQsr1qMy859qiD3nfQyr0llSQTMKI