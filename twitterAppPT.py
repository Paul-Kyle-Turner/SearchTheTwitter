import argparse
import configparser
import sqlite3
import os.path
from os import path

import twitter


class TwitterApp:

    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret):

        self.api = twitter.Api(consumer_key=consumer_key,
                               consumer_secret=consumer_secret,
                               access_token_key=access_token,
                               access_token_secret=access_token_secret,
                               tweet_mode='extended')

    # Write the the newest 200 followers of the specified user name in a file named Twitter_Followers.txt
    def write_followers(self, screen_name):
        results = self.api.GetFollowersPaged(screen_name=screen_name)
        followers = results[2]

        with open("Twitter_Followers.txt", 'w', encoding="utf-8") as file:
            file.write("{} is followed by:\n".format(screen_name))
            for follower in followers:
                file.write("\t{}\n".format(follower.screen_name))

    # Write the last 10 tweets of the specified user to a file named Twitter_Timeline.txt
    def write_timeline(self, screen_name):

        with open("Twitter_Timeline.txt", 'w', encoding="utf-8") as file:
            timeline = self.api.GetUserTimeline(screen_name=screen_name, count=10)

            file.write("Latest tweets from {}:\n\n".format(screen_name))
            for status in timeline:
                file.write("Url:  https://twitter.com/i/web/status/{}\n".format(status.id))
                file.write("Created at: {}\n".format(status.created_at))
                file.write("Tweet: {}\n\n".format(status.full_text))






