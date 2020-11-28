# -*- coding: utf-8 -*-
"""
Created on Sat Nov 21 21:33:26 2020

@author: kaitr
"""

import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
import time

#%% Keys
api_key = 'qGvaPEu1o3TiI5qlLiEnX1AdW'
api_secret_key = 'qkzGqHlCxHGyfNZmd6bITOC9YzFZrzQvcenofuE7XaVwY67lwI'
bearer_token = 'AAAAAAAAAAAAAAAAAAAAAG3mJwEAAAAAKjmDcN3St16GQXL2y2908mjZE%2FQ%3DIOEDzbSMQrSw2jFx9DulaWGMqP3efOAbVdmABFl6NDSIQj7eFh'

#%% Functions

def clean_tweet(tweet): 
        ''' 
        Utility function to clean tweet text by removing links, special characters 
        using simple regex statements. 
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\/\/\S+)", " ", tweet).split())

def get_tweet_sentiment(tweet): 
        ''' 
        Utility function to classify sentiment of passed tweet 
        using textblob's sentiment method 
        '''
        # create TextBlob object of passed tweet text 
        analysis = TextBlob(clean_tweet(tweet))
        # set sentiment 
        if analysis.sentiment.polarity > 0: 
            return 'positive'
        elif analysis.sentiment.polarity == 0: 
            return 'neutral'
        else: 
            return 'negative'

def get_tweets(api, query, count = 100):

    tweets = [] 
  
    # call twitter api to fetch tweets 
    fetched_tweets = api.search(q = query, count = count, lang = 'en')
  
    # parsing tweets one by one 
    for tweet in fetched_tweets: 
        # empty dictionary to store required params of a tweet 
        parsed_tweet = {} 
  
        # saving text of tweet 
        parsed_tweet['text'] = tweet.text 
        # saving sentiment of tweet 
        parsed_tweet['sentiment'] = get_tweet_sentiment(tweet.text) 
  
        # appending parsed tweet to tweets list 
        if tweet.retweet_count > 0: 
            # if tweet has retweets, ensure that it is appended only once 
            if parsed_tweet not in tweets: 
                tweets.append(parsed_tweet)
                
            else: 
                tweets.append(parsed_tweet) 
  
    # return parsed tweets 
    return tweets

#%%

print('Connecting to twitter...')
auth = OAuthHandler(api_key, api_secret_key)

api = tweepy.API(auth)

q1 = "pandemic OR COVID OR coronavirus"

print('Getting tweets... ')
tweets = get_tweets(api, q1, count = 10000)

n = 100

for i in range(n):
    
    print(i + 1, 'out of', n, sep = ' ')
    
    time.sleep(5)
    more_tweets = get_tweets(api, q1, count = 10000)

    for curr_tweet in more_tweets:
        
        tweets.append(curr_tweet)
    
    

positives = 0
negatives = 0
text = ''

for tweet in tweets:
    
    if tweet['sentiment'] == 'positive':
        positives += 1
        
    if tweet['sentiment'] == 'negative':
        negatives += 1
        
    text = tweet['text']

neutrals = len(tweets) - positives - negatives

print('Positives: ', round((positives / len(tweets)) * 100, 2), '%', sep = '')
print('Neutrals: ', round((neutrals / len(tweets)) * 100, 2), '%', sep = '')
print('Negatives: ', round((negatives / len(tweets)) * 100, 2), '%', sep = '')

wordcloud = WordCloud(background_color = 'white').generate(text)

plt.imshow(wordcloud, interpolation = 'bilinear')
plt.axis('off')
plt.show()







