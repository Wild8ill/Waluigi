#! /usr/bin/env python3

import tweepy
from telegram.ext import Updater
import telegram
from datetime import datetime, timedelta
from random import randint


def checkfortweets(tweets,listofwords):
    testword = listofwords.pop()
    capitalisedtestword = testword[0].upper() + testword[1:]
    
    for tweet in tweets:
        if (testword in tweet.text or capitalisedtestword in tweet.text) and (tweet.created_at > (datetime.today() - timedelta(days=1))) and (tweet.user.name == "Wario64" or tweet.user.name == "videogamedeals") and not ("US PSN" in tweet.text) and not ("Best buy" in tweet.text) and not ("best buy" in tweet.text):
            walmod = ["WALUIGI NUMBER ONEEEE!!","WAH!","Wahahaha! Waluigi, number one!","Waluigi win!","Wah hah hah waah!","Waluigi time!"]
            textmessage = walmod[randint(0,len(walmod)-1)] +"\n" + tweet.text
            print(textmessage)
            chatarray = ["REDACTED"]
            print(textmessage)
            for each in chatarray:
                wal_bot.send_message(chat_id=each, text=textmessage)

    if len(listofwords) != 0:
        checkfortweets(tweets,listofwords)


# Twitter API credentials
consumer_key = "REDACTED"
consumer_secret = "REDACTED"
access_key = "REDACTED"
access_secret = "REDACTED"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)

api = tweepy.API(auth, wait_on_rate_limit=True)

# initialising a telegram bot
wal_bot = telegram.Bot("REDACTED")
updater = Updater("REDACTED")
dispatcher = updater.dispatcher
print(wal_bot.get_me())


#gets last checked tweet id to stop spam
with open("recenttweet.txt", "r") as f:
    read_data = f.read()
            
public_tweets = api.home_timeline(read_data) #gets all new tweets from timeline

if public_tweets == []: # if there are no new ones exits
    print("No new tweets")
    exit(0)

firsttweet = public_tweets[0] #the first (at the top aka most recent) tweet, and the one we will
# use to ensure no spam
with open("recenttweet.txt", "w") as f:
    f.write(str(firsttweet.id))

#runs function
checkfortweets(public_tweets,["free","destiny","superhot","cuphead","zelda","Star Wars","star wars","sonic","xenoblade","oneplus","xps"])
