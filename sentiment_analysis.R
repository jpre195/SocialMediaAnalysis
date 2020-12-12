setwd('C:\\Users\\kaitr\\Documents\\GitHub\\SocialMediaAnalysis')


# Required Packages -------------------------------------------------------

library(MASS)
library(ggplot2)
library(fitdistrplus)

# Data Preprocessing ------------------------------------------------------

shoe_tweets = read.csv('shoes2426_tweet_sentiment.csv')
zane_tweets = read.csv('GleasonZane_tweet_sentiment.csv')
russ_tweets = read.csv('RussPhillips11_tweet_sentiment.csv')
brown_tweets = read.csv('sean22_sean_tweet_sentiment.csv')

shoe_tweets$Sentiment = as.numeric(as.character(shoe_tweets$Sentiment))
zane_tweets$Sentiment = as.numeric(as.character(zane_tweets$Sentiment))
russ_tweets$Sentiment = as.numeric(as.character(russ_tweets$Sentiment))
brown_tweets$Sentiment = as.numeric(as.character(brown_tweets$Sentiment))

# EDA ---------------------------------------------------------------------

ggplot(shoe_tweets, aes(x = Sentiment, y = ..density..)) + 
  geom_histogram(fill = 'lightblue', color = 'black') + 
  theme_bw()

ggplot(zane_tweets, aes(x = Sentiment, y = ..density..)) + 
  geom_histogram(fill = 'lightblue', color = 'black') + 
  theme_bw()

ggplot(russ_tweets, aes(x = Sentiment, y = ..density..)) + 
  geom_histogram(fill = 'lightblue', color = 'black') + 
  theme_bw()

ggplot(brown_tweets, aes(x = Sentiment, y = ..density..)) + 
  geom_histogram(fill = 'lightblue', color = 'black') + 
  theme_bw()

# Fit Beta Distribution ---------------------------------------------------

shoe_params = fitdistr(na.omit(shoe_tweets$Sentiment), 'cauchy', start = list(location = 0, scale = 1))
zane_params = fitdistr(na.omit(zane_tweets$Sentiment), 'cauchy', start = list(location = 0, scale = 1))
russ_params = fitdistr(na.omit(russ_tweets$Sentiment), 'cauchy', start = list(location = 0.1, scale = .01), lower = c(-1, 1))
brown_params = fitdistr(na.omit(brown_tweets$Sentiment), 'cauchy', start = list(location = 0, scale = 1))

shoe_params = fitdistr(na.omit(shoe_tweets$Sentiment), 'normal')

ggplot(na.omit(shoe_tweets), aes(x = Sentiment, y = ..density..)) +
  geom_histogram(fill = 'lightblue', color = 'black') +
  stat_function(fun = dnorm, args = list(mean = shoe_params$estimate[1], sd = shoe_params$estimate[2])) +
  theme_bw()

# ggplot(shoe_tweets, aes(x = Sentiment, y = ..density..)) +
#   geom_histogram(fill = 'lightblue', color = 'black') +
#   stat_function(aes(x = Sentiment), fun = dcauchy, args = list(location = shoe_params$estimate[1], scale = shoe_params$estimate[2])) +
#   theme_bw()
# 
# ggplot(zane_tweets, aes(x = Sentiment, y = ..density..)) + 
#   geom_histogram(fill = 'lightblue', color = 'black') + 
#   stat_function(fun = dcauchy, args = list(location = zane_params$estimate[1], scale = zane_params$estimate[2])) +
#   theme_bw()
# 
# ggplot(russ_tweets, aes(x = Sentiment, y = ..density..)) + 
#   geom_histogram(fill = 'lightblue', color = 'black') + 
#   theme_bw()
# 
# ggplot(brown_tweets, aes(x = Sentiment, y = ..density..)) + 
#   geom_histogram(fill = 'lightblue', color = 'black') + 
#   theme_bw()


cat('Shoe probability of positive:', 1 - pcauchy(0, location = shoe_params$estimate[1], scale = shoe_params$estimate[2]), '\n')
cat('Shoe probability of negative:', pcauchy(0, location = shoe_params$estimate[1], scale = shoe_params$estimate[2]), '\n')

cat('Zane probability of positive:', 1 - pcauchy(0, location = zane_params$estimate[1], scale = zane_params$estimate[2]), '\n')
cat('Zane probability of negative:', pcauchy(0, location = zane_params$estimate[1], scale = zane_params$estimate[2]), '\n')

cat('Russ probability of positive:', 1 - pcauchy(0, location = russ_params$estimate[1], scale = russ_params$estimate[2]), '\n')
cat('Russ probability of negative:', pcauchy(0, location = russ_params$estimate[1], scale = russ_params$estimate[2]), '\n')

cat('Brown probability of positive:', 1 - pcauchy(0, location = brown_params$estimate[1], scale = brown_params$estimate[2]), '\n')
cat('Brown probability of negative:', pcauchy(0, location = brown_params$estimate[1], scale = brown_params$estimate[2]), '\n')

cat('Shoe mean tweet: ', mean(na.omit(shoe_tweets$Sentiment)))
cat('Zane mean tweet: ', mean(na.omit(zane_tweets$Sentiment)))
cat('Russ mean tweet: ', mean(na.omit(russ_tweets$Sentiment)))
cat('Brown mean tweet: ', mean(na.omit(brown_tweets$Sentiment)))

cat('Shoe mean tweet: ', mean(rcauchy(10000, location = shoe_params$estimate[1], scale = shoe_params$estimate[2])))
cat('Zane mean tweet: ', mean(rcauchy(10000, location = zane_params$estimate[1], scale = zane_params$estimate[2])))
cat('Russ mean tweet: ', mean(rcauchy(10000, location = russ_params$estimate[1], scale = russ_params$estimate[2])))
cat('Brown mean tweet: ', mean(rcauchy(10000, location = brown_params$estimate[1], scale = brown_params$estimate[2])))


