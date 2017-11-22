import os
import mongoengine
from pymongo import MongoClient
from tweetstake.apps.common.decorators import singleton
from tweetstake.apps.common.domain import DataBaseParameters


class Constants(object):
    MAX_SECONDS_COLLECTION_ITERATIONS = 35
    MAX_SECONDS_WAIT_RESUME_COLLECTION = 720  # 12 minutes
    MAX_INPUT_FILTERS = 15

    DATABASE_CONNECTION_DEFAULT_NAME = 'tweetscollector'
    DATABASE_CONNECTION_DEFAULT_HOST = 'localhost:27017'

    MSG_EXCEPTION_NO_ACCOUNTS = 'There are no registered accounts'
    MSG_EXCEPTION_ACCOUNT_INDEX_OUT_OF_RANGE = 'Account index out of range'
    MSG_EXCEPTION_LIVE_TIME_NOT_EXIST = "It is mandatory to use at least one time-of-life command (-hours or -minutes)"
    MSG_EXCEPTION_LIVE_TIME_NEGATIVE_INTEGER = "It is mandatory that the time of life are a positive integer " \
                                               "number greater than zero"
    MSG_EXCEPTION_FILTER_NOT_EXIST = "It is mandatory to use the '-filter' command"
    MSG_EXCEPTION_ACCOUNTS_FILE_COMMAND_NOT_EXIST = "it is mandatory to use the '-account_file' command"
    MSG_EXCEPTION_TWITTER_RESPONSE = 'Twitter response error: '
    MSG_EXCEPTION_EXCEEDED_MAX_FILTERS = 'You can only add {0} filters at most'.format(MAX_INPUT_FILTERS)
    MSG_EXCEPTION_DOMAIN_ATTRIBUTES_NOT_MATCH_CSV_FIELDS = "Domain model attributes do not match the fields in the" \
                                                           " CSV file"
    MSG_HELP_FILTER_ACCOUNTS_FILE = "Accounts CSV file path"
    MSG_HELP_FILTER_COMMAND = "Tweeter API query string (https://dev.twitter.com/rest/public/search)"
    MSG_HELP_LIVE_HOURS_COMMAND = "Duration of the collection in hours (summable to '-minutes' command)"
    MSG_HELP_LIVE_MINUTES_COMMAND = "Duration of the collection in minutes (summable to '-hours' command)"
    MSG_HELP_DATABASE_NAME_COMMAND = "MongoDB database name (by default is {0})".format(DATABASE_CONNECTION_DEFAULT_NAME)
    MSG_HELP_DATABASE_HOST_COMMAND = "MongoDB database host (by default is {0})".format(DATABASE_CONNECTION_DEFAULT_HOST)
    MSG_EXCEEDED_TWITTER_RATE_LIMIT = 'Exceeded Twitter Rate Limit'
    MSG_ACCOUNT_RELIEVED = 'User account RELIEVED'
    MSG_EXIT_APP = 'Press Ctrl+{0} to exit'
    MSG_TWEETS_COLLECTED = "Tweets collected so far: "
    MSG_COLLECTION_FINISHED = "Collection FINISHED"
    MSG_PAUSE_COLLECTION = "Pause the collection"
    MSG_RESUME_COLLECTION = "Resume the collection"
    MSG_CURRENT_ACCOUNT_USERNAME = "Current account username: "
    MSG_EXCEEDED_RATE_LIMIT_REPEATEDLY = "Exceeded the twitter rate limit repeatedly. It is possible to avoid " \
                                         "this if you enter more accounts. It is mandatory to pause the collection " \
                                         "for {0} minutes".format(MAX_SECONDS_WAIT_RESUME_COLLECTION / 60)

    COMMAND_ACCOUNTS_FILE = '-accounts_file'
    COMMAND_FILTER = '-filter'
    COMMAND_LIVE_HOURS = '-hours'
    COMMAND_LIVE_MINUTES = '-minutes'
    COMMAND_DATABASE_NAME = '-db_name'
    COMMAND_DATABASE_HOST = '-db_host'

    ARG_ACCOUNTS_FILE_COMMAND = '<path>'
    ARG_FILTER_COMMAND = '<string>'
    ARG_LIVE_HOURS_COMMAND = '<integer>'
    ARG_LIVE_MINUTES_COMMAND = '<integer>'
    ARG_DATABASE_NAME_COMMAND = '<string>'
    ARG_DATABASE_HOST_COMMAND = '<string>'

    PARAMETER_INTERVAL_SCHEDULER = 'interval'
    PARAMETER_CSV_DELIMITER = ','
    PARAMETER_CSV_QUOTECHAR = '"'
    PARAMETER_CSV_SKIPINITIALSPACE = True

    TIME_CONTROL_RATE_LIMIT_EXCEPTION_IN_SECONDS = 5

    DATABASE_HOST = '192.168.43.98:8082'

    FORMAT_LOGGING_BASE = '%(asctime)s - %(levelname)s: %(message)s'
    FORMAT_LOGGING_DATETIME = '%Y-%m-%d %H:%M:%S'
    FORMAT_DESERIALIZE_TWEET_DATETIME = '%a %b %d %H:%M:%S +0000 %Y'

    MODE_OPEN_FILE_W = 'w'
    MODE_OPEN_FILE_R = 'r'
    MODE_OPEN_FILE_R_W = 'r+'


class HttpHelper(object):
    @staticmethod
    def url_encoding(string: str) -> str:
        result = string.replace('#', '%23').replace('@', '%40').replace('-', '%2D').replace(':', '%3A') \
            .replace('"', '%22').replace(' ', '+')
        return result


class OSHelper(object):
    @staticmethod
    def get_exit_key() -> str:
        return 'Break' if os.name == 'nt' else 'C'


@singleton
class DataBaseUtil(object):

    connection: MongoClient = None

    def connect(self, database_parameters: DataBaseParameters) -> None:

        if database_parameters.database_name is None:
            database_parameters.database_name = Constants.DATABASE_CONNECTION_DEFAULT_NAME

        if database_parameters.database_host is None:
            database_parameters.database_host = Constants.DATABASE_CONNECTION_DEFAULT_HOST

        if DataBaseUtil.connection is None:
            DataBaseUtil.connection = mongoengine.connect(
                db=database_parameters.database_name,
                host=database_parameters.database_host
            )


class InfoException(Exception):
    pass


class ExceededRateLimitRepeatedly(Exception):
    pass
