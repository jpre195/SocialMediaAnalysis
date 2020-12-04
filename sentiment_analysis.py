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
#        # set sentiment 
#        if analysis.sentiment.polarity > 0.2: 
#            return 'positive'
#        elif analysis.sentiment.polarity < 0.2 and analysis.sentiment.polarity > -0.2: 
#            return 'neutral'
#        else: 
#            return 'negative'
        
        return analysis.sentiment.polarity

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

#q1 = "pandemic OR COVID OR coronavirus"
##q1 = "lang:en"
#
#print('Getting tweets... ')
#tweets = get_tweets(api, q1, count = 10000)
#
#n = 50
#
#for i in range(n):
#    
#    print(i + 1, 'out of', n, sep = ' ')
#    
#    time.sleep(30)
#    more_tweets = get_tweets(api, q1, count = 10000)
#
#    for curr_tweet in more_tweets:
#        
#        tweets.append(curr_tweet)
#    
#    
#    
##positives = 0
##negatives = 0
#text = ''
#
#for tweet in tweets:
#    
##    if tweet['sentiment'] == 'positive':
##        positives += 1
##        
##    if tweet['sentiment'] == 'negative':
##        negatives += 1
#        
#    text = text + tweet['text']
#
##neutrals = len(tweets) - positives - negatives
#
##print('Positives: ', round((positives / len(tweets)) * 100, 2), '%', sep = '')
##print('Neutrals: ', round((neutrals / len(tweets)) * 100, 2), '%', sep = '')
##print('Negatives: ', round((negatives / len(tweets)) * 100, 2), '%', sep = '')
#
#stop_words = ['https', 'RT', 'http', 'will', 'know', 're', 'let'] + list(STOPWORDS)
#
#wordcloud = WordCloud(stopwords = stop_words, background_color = 'white').generate(text)
#
#plt.imshow(wordcloud, interpolation = 'bilinear')
#plt.axis('off')
#plt.show()


#%%

#user = 'shoes2426'
#user = 'RussPhillips11'
user = 'GleasonZane'


def user_word_cloud(user):
    stop_words = ['one', 'time', 'https', 'RT', 'http', 'will', 'know', 're', 'let'] + list(STOPWORDS)
    
    tweets = []
    
    for tweet in tweepy.Cursor(api.user_timeline, screen_name = user).items():
        
        parsed_tweet = {}
        
        parsed_tweet['text'] = clean_tweet(tweet.text)
        parsed_tweet['sentiment'] = get_tweet_sentiment(tweet.text)
        
        tweets.append(parsed_tweet)
        
    text = ''
    
    for tweet in tweets:
    
        text = text + ' ' + tweet['text']
    
    
    wordcloud = WordCloud(stopwords = stop_words, background_color = 'white').generate(text)
    
    plt.imshow(wordcloud, interpolation = 'bilinear')
    plt.axis('off')
    #plt.show()
    plt.savefig(user + '.png', dpi = 2000)
    
    return tweets

users = ['shoes2426', 'RussPhillips11', 'GleasonZane']

for user in users:
    
    user_word_cloud(user)

#%%

def user_hashtag_word_cloud(username):
    stop_words = ['one', 'time', 'https', 'RT', 'http', 'will', 'know', 're', 'let'] + list(STOPWORDS)
    
    tweets = []
    
    for tweet in tweepy.Cursor(api.user_timeline, screen_name = username).items():
        
        parsed_tweet = {}
        
        hashtags = tweet.entities.get('hashtags')
        
        if len(hashtags) > 0:
            
            for i in range(len(hashtags)):
                
#                parsed_tweet['text'] = clean_tweet(hashtags[i]['text'])
                parsed_tweet['text'] = hashtags[i]['text']
                
                parsed_tweet['sentiment'] = get_tweet_sentiment(hashtags[i]['text'])
                
                tweets.append(parsed_tweet)
        
#        parsed_tweet['text'] = clean_tweet(tweet.entities.get('hashtags')['text'])
#        parsed_tweet['sentiment'] = get_tweet_sentiment(tweet.text)
        
#        tweets.append(parsed_tweet)
        
    text = ''
    
    for tweet in tweets:
    
        text = text + ' ' + tweet['text']
    
    
    wordcloud = WordCloud(collocations = False, stopwords = stop_words, background_color = 'white').generate(text)
    
    plt.imshow(wordcloud, interpolation = 'bilinear')
    plt.axis('off')
    #plt.show()
    plt.savefig(username + '_hashtags' + '.png', dpi = 2000)
    
    return tweets
    
    
##user = 'shoes2426'
#user = 'RussPhillips11'
##user = 'GleasonZane'

users = ['shoes2426', 'RussPhillips11', 'GleasonZane']

test1 = user_hashtag_word_cloud(user)

for user in users:
    
    user_hashtag_word_cloud(user)


#%%

def user_mentions_word_cloud(username):
    stop_words = ['one', 'time', 'https', 'RT', 'http', 'will', 'know', 're', 'let'] + list(STOPWORDS)
    
    tweets = []
    
    for tweet in tweepy.Cursor(api.user_timeline, screen_name = username).items():
        
        parsed_tweet = {}
        
        user_mentions = tweet.entities['user_mentions']
        
        if len(user_mentions) > 0:
            
            for i in range(len(user_mentions)):
                
                parsed_tweet['text'] = user_mentions[i]['screen_name']
                
                parsed_tweet['sentiment'] = 0
                
                tweets.append(parsed_tweet)
        
        
    text = ''
    
    for tweet in tweets:
    
        text = text + ' ' + tweet['text']
    
    
    wordcloud = WordCloud(collocations = False, background_color = 'white').generate(text)
    
    plt.imshow(wordcloud, interpolation = 'bilinear')
    plt.axis('off')
    #plt.show()
    plt.savefig(username + '_user_mentions' + '.png', dpi = 2000)
    
    return tweets

users = ['shoes2426', 'RussPhillips11', 'GleasonZane']

for user in users:
    
    user_mentions_word_cloud(user)



