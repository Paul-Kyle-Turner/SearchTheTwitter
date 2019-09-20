import argparse
import configparser
from twitterAppPT import TwitterApp
import threading
from signal import signal, SIGINT
import sys
import time

DEFAULT_CONFIG = 'config.ini'
ctrl_c = False
search_threads = []


def handel_ctrl_c(signal_received, frame):
    # used to always exit on a sleep so that no thread gets cut off
    global ctrl_c
    global search_threads
    ctrl_c = True
    while not search_threads:
        for search_thread in search_threads:
            if not search_thread.is_alive():
                search_threads.remove(search_thread)
    sys.exit(0)


def search_thread_function(searcher, query):
    searcher.search(query)


def settings(args):
    # Settings configuration, defaults can be changed in the config file
    config = configparser.ConfigParser()
    if args.config_file is None:
        config.read(DEFAULT_CONFIG)
    else:
        config.read(args.config_file)

    if args.config_file is not None or \
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

    if args.quantum is None:
        quantum = config['CONTINUE']['quantum']
    else:
        quantum = args.quantum

    return consumer_key, consumer_secret, access_token, access_token_secret, \
        text_followers_filename, text_timeline_filename, \
        json_followers_filename, json_timeline_filename, database_path, quantum


def main():
    signal(SIGINT, handel_ctrl_c)
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

    parser.add_argument('-gd', '--gather_data', action='store_true',
                        help='Gather data from google results for every quantum of time')
    parser.add_argument('-q', '--quantum', type=int,
                        help='A quantum of time for gathering data')

    parser.add_argument('-mq', '--multi_query', nargs='*',
                        help='''flag used to grab many different keyword tweets along with the first query.
                        Multi_query must be used with gather_data flag''')

    args = parser.parse_args()
    print(args)

    consumer_key, consumer_secret, access_token, access_token_secret, \
        text_followers_filename, text_timeline_filename, \
        json_followers_filename, json_timeline_filename, database_path, quantum = settings(args)

    if args.gather_data is True:
        args.use_database = True
        args.use_text = False
        args.use_json = False

    twitter = TwitterApp(consumer_key, consumer_secret, access_token, access_token_secret,
                         text_followers_filename, text_timeline_filename,
                         json_followers_filename, json_timeline_filename, database_path,
                         args.use_text, args.use_json, args.use_database,
                         args.use_timeline, args.use_followers)

    count = 0
    q_list = []
    if args.multi_query:
        q_list = args.multi_query
        q_list.append(args.query)
    else:
        q_list.append(args.query)

    print(q_list)

    # Run the search
    if args.gather_data:
        while not ctrl_c:
            global search_threads
            for query in q_list:
                search_thread = threading.Thread(target=search_thread_function,
                                                 args=(twitter, query), name='search_thread')
                search_thread.start()
                search_threads.append(search_thread)
            count = count + 1
            print(f"Gathering data from Twitter for {count} times")
            # get the number of min for the thread to wait
            sleep_time = int(quantum) * 60
            time.sleep(sleep_time)
    else:
        twitter.search(args.query)


if __name__ == '__main__':
    main()
