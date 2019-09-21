# SearchTheTwitter
Quick twitter search from python, results in either json or human readable format and sqlite database.  This application
can be used to gather data after a given amount of time and store that data within a database.

Default output is of the timeline of a given keyword.

Config file :\
    The configuration file can be changed with the flag -c.  The configuration file must follow the same format as the
    config.ini file.

Keys:
    The Twitter api needs to be supplied with four keys.  Each of the keys can be changed with the following flags :\
        -ck [arg], the consumer key \
        -cs [arg], the consumer secret\
        -at [arg], the access token\
        -ats [arg], the access secret token\
        Each of these parameters needs to be supplied for any of them to be used.

Timeline and/or Followers:\
    Either one or both of the -uf, -utl flags can be given to collect data on either the followers or the timeline.\
        -uf, use followers flag\
        -utl, use timeline flag

Json options:\
    To use a json format the flag -uj.  To change the file used for storing either the timeline data or followers data
    use the flags :\
        -jf [arg], used to change the json output file for the followers data\
        -jt [arg], used to change the json output file for the timeline data\

Database options:\
    To use a database the flag -ud is given.  To change the database path use the flag -d [arg].

Text options:\
    To use a text format the flag -ut.  To change the file used for storing either the timeline data or followers data
    use the flags :\
        -tf [arg], used to change the json output file for the followers data\
        -tt [arg], used to change the json output file for the timeline data

Gathering data:\
    To gather data for extended periods of time use the -gd flag.  For each quantum of time run the query again storing
    any new data to the database.  The database must be used for this option and will be automatically used if this
    option is picked.\
        -q [arg], used to change the quantum of time difference between query. (note this is by default set at 15 min,
         if a value lower then 15 min is used the Twitter api may exceed the given allowances for a basic account)

Multiple Query:\
    Gather data on multiple keywords at the same time with the used of the -mq [args*] flag.