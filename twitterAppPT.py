from sqlite3 import Error
from dbSQLite import SqLiteTwit
from dbSQLite import SqLite
import json

import twitter


class TwitterApp:

    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret,
                 text_followers_filename, text_timeline_filename,
                 json_followers_filename, json_timeline_filename, database_path,
                 use_text, use_json, use_database, timeline, followers, tables=None, twit=True):
        self.text_followers_filename = text_followers_filename
        self.text_timeline_filename = text_timeline_filename
        self.json_followers_filename = json_followers_filename
        self.json_timeline_filename = json_timeline_filename
        self.database_path = database_path
        self.use_text = use_text
        self.use_json = use_json
        self.use_database = use_database
        self.use_timeline = timeline
        self.use_followers = followers
        self.api = twitter.Api(consumer_key=consumer_key,
                               consumer_secret=consumer_secret,
                               access_token_key=access_token,
                               access_token_secret=access_token_secret,
                               tweet_mode='extended')

        if use_database and database_path is not None:
            if tables is not None and twit:
                # use a different SqLite database set up
                # this will require all commands to go through the execute command method
                self.db = self.sql_db_setup_custom(SqLiteTwit, database_path, tables)
            elif tables is not None:
                # use different tables then the three defaults
                # warning this can have unintended effects on the default use of SqLiteGoog
                self.db = self.sql_db_setup_custom(SqLite, database_path, tables)
            else:
                self.db = self.sql_db_setup(SqLiteTwit, database_path)

    def search(self, screen_name):
        if self.use_timeline:
            timeline = self.timeline(screen_name)
            self.to_output_timeline(screen_name, timeline)
        if self.use_followers:
            followers = self.followers(screen_name)
            self.to_output_followers(screen_name, followers)

    def followers(self, screen_name):
        return self.api.GetFollowersPaged(screen_name=screen_name)[2]

    def timeline(self, screen_name, count=10):
        return self.api.GetUserTimeline(screen_name=screen_name, count=count)

    def sql_db_setup(self, sql_class, database_path):
        try:
            self.db = sql_class(database_path)
        except Error as e:
            print(e)
            self.db = None
        return self.db

    def sql_db_setup_custom(self, sql_class, database_path, tables):
        try:
            self.db = sql_class(tables, database_path)
        except Error as e:
            print(e)
            self.db = None
        return self.db

    def to_output_followers(self, screen_name, followers):
        if not self.use_json and not self.use_database:
            self.use_text = True
        if self.use_json:
            self.to_json_file(followers, False)
        if self.use_text:
            self.write_followers(screen_name, followers)
        if self.use_database:
            self.to_sql_db_followers(screen_name, followers)
        return followers

    def to_output_timeline(self, screen_name, timeline):
        if not self.use_json and not self.use_database:
            self.use_text = True
        if self.use_json:
            self.to_json_file(timeline)
        if self.use_text:
            self.write_timeline(screen_name, timeline)
        if self.use_database:
            self.to_sql_db_timeline(screen_name, timeline)
        return timeline

    def to_json_file(self, result, timeline=True):
        if timeline:
            with open(self.json_timeline_filename, 'w') as file:
                json.dump(result, file)
        else:
            with open(self.json_followers_filename, 'w') as file:
                json.dump(result, file)

    def to_sql_db_timeline(self, screen_name, timeline):
        screen_name_id = self.db.create_screen_name(screen_name)
        for status in timeline:
            self.db.create_timeline(status.full_text, status.id, status.created_at, screen_name_id)

    def to_sql_db_followers(self, screen_name, followers):
        screen_name_id = self.db.create_screen_name(screen_name)
        for follower in followers:
            self.db.create_follower(follower.screen_name, screen_name_id)

    # Write the the newest 200 followers of the specified user name in a file named Twitter_Followers.txt
    def write_followers(self, screen_name, followers):
        with open(self.text_followers_filename, 'w', encoding="utf-8") as file:
            file.write("{} is followed by:\n".format(screen_name))
            for follower in followers:
                file.write("\t{}\n".format(follower.screen_name))

    # Write the last 10 tweets of the specified user to a file named Twitter_Timeline.txt
    def write_timeline(self, screen_name, timeline):
        with open(self.text_timeline_filename, 'w', encoding="utf-8") as file:
            file.write("Latest tweets from {}:\n\n".format(screen_name))
            for status in timeline:
                file.write("Url:  https://twitter.com/i/web/status/{}\n".format(status.id))
                file.write("Created at: {}\n".format(status.created_at))
                file.write("Tweet: {}\n\n".format(status.full_text))
