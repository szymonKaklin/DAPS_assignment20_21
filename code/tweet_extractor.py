# REQUIRED IMPORTS
# This script requires tweepy - a python wrapper for the Twitter API
import tweepy
import pickle
import numpy as np
import pandas as pd
import json

# TWITTER DEVELOPER ACCOUNT KEYS
# enter the 4 appropriate keys received from Twitter developer account
consumer_key = ''
consumer_secret = ''

access_token = ''
access_token_secret = ''

# TWITTER API AUTHORIZATION
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# adding wait on rate limit so when we hit it we continue
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

# creating function which gets the tweets in batches of 100 at a time
# this is the maximum the twitter API allows, before we can get another batch
# then, the only restriction is the number of calls to API in each 15 min window
def get_tweets(tweet_IDs, api):
	full_tweets = []
	tweet_count = len(tweet_IDs)
	try:
		for i in range((tweet_count // 100) + 1):
			#print('\nin loop\n')
			# this also catches the last tweet group if it is less than 100
			# ***BUG*** this breaks api call if id list is exactly a multiple of 100
			end = min((i + 1) * 100, tweet_count)
			full_tweets.extend(api.statuses_lookup(id_=tweet_IDs[i * 100:end], tweet_mode="extended"))
			print('\rGot batch: ', i, '/', tweet_count//100, end="", flush=True)
		return full_tweets
	except tweepy.TweepError:
		print('error: ', tweepy.TweepError)

# Opening tweet-ids text file
ids = np.loadtxt("tweet-ids-004.txt", dtype=str)
ids = list(ids)

# function works only if not multiply of 100 - an oversight, but we can just start from second
# tweet id
ids = ids[1:]

# Getting all tweets, and putting them in json file
all_tweets = get_tweets(ids, api)

data_json = json.dumps([tweet._json for tweet in all_tweets])

# Converting this json into a pandas dataframe, pickling it, and saving
df = pd.read_json(data_json, orient='records')
df.to_pickle('./tweets4_df.pkl')


# DATASET LINKS
# Each of these is a link to the specific TweetSets datasets i tested/used

# tweet-ids-004.txt dataset (finance terms based of paper 2017-2020) (200,000)
# http://tweetsets.library.gwu.edu/dataset/b8066f0e

# tweet-ids-003.txt dataset (all news from 2017-2020) (100,000)
# http://tweetsets.library.gwu.edu/dataset/c2c3277b

# tweet-ids-002.txt (all news from 2009-2020) (100,000)
# https://tweetsets.library.gwu.edu/dataset/a779290b

# tweet-ids-001.txt (2017-2020 just #Apple, #AAPL) (aprox. 12000)
# http://tweetsets.library.gwu.edu/dataset/c34cd237


