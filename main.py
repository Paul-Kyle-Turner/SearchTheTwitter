import argparse
import configparser
from twitterAppPT import TwitterApp

DEFAULT_CONFIG = 'config.ini'


def settings(args):
    # Settings configuration, defaults can be changed in the config file
    config = configparser.ConfigParser()
    if args.config_file is None:
        config.read(DEFAULT_CONFIG)
    else:
        config.read(args.config_file)

    if args.config_file is None or \
            args.c_key is not None and \
            args.cs_key is not None and \
            args.at_key is not None and \
            args.ats_key is not None:
        consumer_key = args.c_key
        consumer_secret = args.cs_key
        access_token = args.at_key
        access_token_secret = args.ats_key
    else:
        consumer_key = config['DEFAULT']['consumerKey']
        consumer_secret = config['DEFAULT']['consumerSecret']
        access_token = config['DEFAULT']['accessToken']
        access_token_secret = config['DEFAULT']['accessTokenSecret']

    # set the output files locations
    if args.text_followers is None:
        text_followers_filename = config['DEFAULT']['textFollowersOutputFile']
    else:
        text_followers_filename = args.text
    if args.text_timeline is None:
        text_timeline_filename = config['DEFAULT']['textTimelineOutputFile']
    else:
        text_timeline_filename = args.text

    if args.json_followers is None:
        json_followers_filename = config['DEFAULT']['jsonFollowersOutputFile']
    else:
        json_followers_filename = args.json
    if args.json_timeline is None:
        json_timeline_filename = config['DEFAULT']['jsonTimelineOutputFile']
    else:
        json_timeline_filename = args.json

    if args.database is None:
        database_path = config['SQLITE']['databasePath']
    else:
        database_path = args.database

    return consumer_key, consumer_secret, access_token, access_token_secret, \
        text_followers_filename, text_timeline_filename, \
        json_followers_filename, json_timeline_filename, database_path


def main():
    # Argument parser for simple settings changes
    parser = argparse.ArgumentParser()
    parser.add_argument('query', help='Search query')
    parser.add_argument('-c', '--config_file',
                        help='Path to non-default config file')

    parser.add_argument('-ck', '--c_key',
                        help='Use a different consumer key then the default in config')
    parser.add_argument('-cs', '--cs_key',
                        help='Use a different consumer secret key then the default in config')
    parser.add_argument('-at', '--at_key',
                        help='Use a different access token then the default in config')
    parser.add_argument('-ats', '--ats_key',
                        help='Use a different access token secret key then the default in config')

    parser.add_argument('-uj', '--use_json', action='store_true',
                        help='Use a json for the query result')
    parser.add_argument('-jf', '--json_followers',
                        help='Change the json followers file path')
    parser.add_argument('-jt', '--json_timeline',
                        help='Change the json timeline file path')

    parser.add_argument('-ud', '--use_database', action='store_true',
                        help='Use a database for the query result')
    parser.add_argument('-d', '--database',
                        help='set a database path')

    parser.add_argument('-ut', '--use_text', action='store_true',
                        help='Use text for output')
    parser.add_argument('-tf', '--text_followers',
                        help='set a text followers path')
    parser.add_argument('-tt', '--text_timeline',
                        help='set a text timeline path')

    parser.add_argument('-uf', '--use_followers', action='store_true',
                        help='get the followers of a given screen name')
    parser.add_argument('-utl', '--use_timeline', action='store_true',
                        help='get the timeline for a given screen name')
    args = parser.parse_args()
    print(args)

    consumer_key, consumer_secret, access_token, access_token_secret, \
        text_followers_filename, text_timeline_filename, \
        json_followers_filename, json_timeline_filename, database_path = settings(args)

    twitter_app = TwitterApp(consumer_key, consumer_secret, access_token, access_token_secret,
                             text_followers_filename, text_timeline_filename,
                             json_followers_filename, json_timeline_filename, database_path,
                             args.use_text, args.use_json, args.use_database,
                             args.use_timeline, args.use_followers)


if __name__ == '__main__':
    main()
