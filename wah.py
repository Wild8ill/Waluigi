#! /usr/bin/env python3

import tweepy
from telegram.ext import Updater
import telegram
from datetime import datetime, timedelta
from random import randint
import requests
from bs4 import BeautifulSoup
import json
import re

def scrape_wishlist(username):
    url = "https://store.steampowered.com/wishlist/id/{!s}/#sort=order".format(username)
    print(url)
    r = requests.get(url)
    soup = BeautifulSoup(r.text,'html.parser')
    wishlist_games = ["free"]
    for link in soup.find_all('script'):
        if "g_rgAppInfo" in link.text:
            array_of_vars = link.text.splitlines()
            for each in array_of_vars:
                if "g_rgAppInfo" in each:
                    formatted_string = each.strip()[18:len(each)-2] # exists for a reason, the reason is too long to explain
                    objects = json.loads(formatted_string)
                    for each_game in objects:
                        name_of_the_game =(objects[each_game]["name"])
			#format the name to aid in searching tweets
                        name_of_the_game = re.sub('[^A-Za-z0-9\'.,! ]','',name_of_the_game)
                        name_of_the_game = name_of_the_game.lower().strip()
			#add completed string to the list
                        wishlist_games.append(name_of_the_game)
    return wishlist_games

def verify_tweets(tweets,whitelist,blacklist,users):

    for tweet in tweets:
        tweet_text = tweet.text.lower()
        print(tweet_text)
        state = False
        for each_word in whitelist:
            if each_word in tweet_text:
                print(each_word)
                state = True
        for each_word in blacklist:
            if each_word in tweet_text:
                state = False
        for each_user in users:
            if each_user == tweet.user.name:
                userstatus = True
                break
        #setup waluigi sayings
        walmod = ["WALUIGI NUMBER ONEEEE!!","WAH!","Wahahaha! Waluigi, number one!","Waluigi win!","Wah hah hah waah!","Waluigi time!"]
        #setup list of chat users
        chatarray = ["REDACTED"]
        if state == True and userstatus == True:
            textmessage = walmod[randint(0,len(walmod)-1)] +"\n" + tweet.text
            #print(textmessage)
            for each in chatarray:
                    wal_bot.send_message(chat_id=each, text=textmessage)


# Twitter API credentials
consumer_key = "REDACTED"
consumer_secret = "REDACTED"
access_key = "REDACTED"
access_secret = "REDACTED"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)

api = tweepy.API(auth, wait_on_rate_limit=True)

# Initialising a telegram bot

wal_bot = telegram.Bot("REDACTED")
updater = Updater("REDACTED")
dispatcher = updater.dispatcher
print(wal_bot.get_me())

# Creates and initialises the required whitelist, blacklist, and verified_users variables

whitelist = ["free","destiny","cuphead","zelda","star wars","sonic","xenoblade"]
blacklist = ["us psn","best buy"]
verified_users = ["Wario64","videogamedeals"]


# Gets last checked tweet id to stop spam

with open("recenttweet.txt", "r") as f:
    read_data = f.read()
            
public_tweets = api.home_timeline(read_data) # Gets all new tweets from timeline

if public_tweets == []: # Gf there are no new ones exits the program
    print("No new tweets")
    exit(0)

firsttweet = public_tweets[0] # The first (at the top aka most recent) tweet, and the one we will
# use to ensure no spam
with open("recenttweet.txt", "w") as f:
    f.write(str(firsttweet.id))

# Runs functions

whitelist += scrape_wishlist("REDACTED")
verify_tweets(public_tweets,whitelist,blacklist,verified_users)

