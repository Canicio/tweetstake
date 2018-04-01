import argparse
import sched
import threading
import time
from datetime import datetime, timedelta
from tweetstake.apps.common.domain import DataBaseParameters
from tweetstake.apps.common.util import Constants, OSHelper, InfoException, ExceededRateLimitRepeatedly, DataBaseUtil
from tweetstake.apps.common.config import Log
from tweetstake.apps.csv.service import CsvService
from tweetstake.apps.twitter.domain import TwitterAccount, Tweet, AccountsManager
from tweetstake.apps.twitter.service import TwitterApiService, TweetService
from apscheduler.schedulers.background import BackgroundScheduler
from typing import List
from tweepy import TweepError


class App(object):
    """App class containing the main method"""

    collection_completed: bool = False
    unforeseen_error: bool = False
    pause_job: bool = False
    accounts_manager: AccountsManager

    @staticmethod
    def main() -> None:
        """Main method"""

        scheduler: BackgroundScheduler = None
        accounts_list: List[TwitterAccount]
        parser: argparse.ArgumentParser
        completed: bool
        unexpected_error: bool
        live_in_hours: int
        live_in_minutes: int
        datetime_limit: datetime
        timer: scheduler

        try:

            # Get input arguments
            parser = argparse.ArgumentParser()
            parser.add_argument(Constants.COMMAND_ACCOUNTS_FILE, metavar=Constants.ARG_ACCOUNTS_FILE_COMMAND,
                                nargs=1, type=str, help=Constants.MSG_HELP_FILTER_ACCOUNTS_FILE)
            parser.add_argument(Constants.COMMAND_FILTER, metavar=Constants.ARG_FILTER_COMMAND, nargs='+',
                                type=str, help=Constants.MSG_HELP_FILTER_COMMAND)
            parser.add_argument(Constants.COMMAND_LIVE_HOURS, metavar=Constants.ARG_LIVE_HOURS_COMMAND, nargs=1,
                                type=int, help=Constants.MSG_HELP_LIVE_HOURS_COMMAND)
            parser.add_argument(Constants.COMMAND_LIVE_MINUTES, metavar=Constants.ARG_LIVE_MINUTES_COMMAND, nargs=1,
                                type=int, help=Constants.MSG_HELP_LIVE_MINUTES_COMMAND)
            parser.add_argument(Constants.COMMAND_DATABASE_NAME, metavar=Constants.ARG_DATABASE_NAME_COMMAND, nargs=1,
                                type=str, help=Constants.MSG_HELP_DATABASE_NAME_COMMAND)
            parser.add_argument(Constants.COMMAND_DATABASE_HOST, metavar=Constants.ARG_DATABASE_HOST_COMMAND, nargs=1,
                                type=str, help=Constants.MSG_HELP_DATABASE_HOST_COMMAND)
            args = parser.parse_args()

            # Check input arguments
            if not args.hours and not args.minutes:
                raise InfoException(Constants.MSG_EXCEPTION_LIVE_TIME_NOT_EXIST)
            if (args.hours and args.hours[0] < 0) or (args.minutes and args.minutes[0] < 0):
                raise InfoException(Constants.MSG_EXCEPTION_LIVE_TIME_NOT_EXIST)
            if not args.accounts_file:
                raise InfoException(Constants.MSG_EXCEPTION_ACCOUNTS_FILE_COMMAND_NOT_EXIST)
            if not args.filter:
                raise InfoException(Constants.MSG_EXCEPTION_FILTER_NOT_EXIST)
            if len(args.filter) > 10:
                raise InfoException(Constants.MSG_EXCEPTION_EXCEEDED_MAX_FILTERS)

            # Get accounts from csv file
            accounts_list = CsvService().read_objects_list(args.accounts_file[0], TwitterAccount)
            App.accounts_manager = AccountsManager()
            App.accounts_manager.accounts_list = accounts_list

            # Get parameters from the database if there are
            db_parameters = DataBaseParameters()
            if args.db_name:
                db_parameters.database_name = args.db_name[0]
            if args.db_host:
                print(args.db_host)
                db_parameters.database_host = args.db_host[0]
            DataBaseUtil().connect(db_parameters)

            # Launch collection job
            scheduler = BackgroundScheduler(logger=Log.logger)
            live_in_minutes = args.minutes[0] if args.minutes else 0
            live_in_hours = args.hours[0] if args.hours else 0
            datetime_limit = datetime.now() + timedelta(minutes=live_in_minutes, hours=live_in_hours)
            App.collect(args.filter, datetime_limit)
            scheduler.add_job(App.collect, Constants.PARAMETER_INTERVAL_SCHEDULER,
                              seconds=Constants.MAX_SECONDS_COLLECTION_ITERATIONS,
                              args=(args.filter, datetime_limit))
            scheduler.start()

            # Keeps the main thread alive while collection job is working. When the job is finished,
            # the main thread will end
            Log.logger.info(Constants.MSG_EXIT_APP.format(OSHelper.get_exit_key()))
            lock = threading.RLock()
            with lock:
                completed = App.collection_completed
                unexpected_error = App.unforeseen_error
            while not completed and not unexpected_error:
                time.sleep(2)
                with lock:
                    completed = App.collection_completed
                    unexpected_error = App.unforeseen_error
                    if App.pause_job:
                        Log.logger.info(Constants.MSG_PAUSE_COLLECTION)
                        scheduler.pause()
                        App.pause_job = False
                        timer = sched.scheduler(time.time, time.sleep)
                        timer.enter(Constants.MAX_SECONDS_WAIT_RESUME_COLLECTION, 1, App.resume_collection,
                                    argument=(scheduler,))
                        timer.run()

            scheduler.shutdown()
            if completed:
                Log.logger.info(Constants.MSG_COLLECTION_FINISHED)

        except (KeyboardInterrupt, SystemExit):
            if scheduler:
                scheduler.shutdown()
        except Exception as err:
            Log.logger.error(err)

    @staticmethod
    def collect(criteria_list: List[str], datetime_limit: datetime) -> None:
        """Tweets collect method"""

        tweets_list: List[Tweet]

        try:

            if datetime.now() < datetime_limit:
                tweets_list = TwitterApiService().get_tweets_by_criteria_list(criteria_list, App.accounts_manager)
                TweetService().insert_tweets_list(tweets_list)
                Log.logger.info(Constants.MSG_TWEETS_COLLECTED + str(TweetService().get_tweets_count()))
            else:
                with threading.RLock():
                    App.collection_completed = True

        except ExceededRateLimitRepeatedly:
            Log.logger.warning(Constants.MSG_EXCEEDED_RATE_LIMIT_REPEATEDLY)
            with threading.RLock():
                App.pause_job = True
        except TweepError as err:
            Log.logger.error(Constants.MSG_EXCEPTION_TWITTER_RESPONSE + err.reason)
            with threading.RLock():
                App.unforeseen_error = True
        except Exception as err:
            Log.logger.error(err)
            with threading.RLock():
                App.unforeseen_error = True

    @staticmethod
    def resume_collection(scheduler: BackgroundScheduler):
        with threading.RLock():
            Log.logger.info(Constants.MSG_RESUME_COLLECTION)
            scheduler.resume()


if __name__ == '__main__':
    App.main()
