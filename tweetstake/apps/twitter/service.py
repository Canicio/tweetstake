import tweepy
from typing import List
from tweepy import API, OAuthHandler, RateLimitError
from tweetstake.apps.common.decorators import singleton
from tweetstake.apps.common.domain import DataBaseParameters
from tweetstake.apps.common.util import Constants, InfoException, ExceededRateLimitRepeatedly, DataBaseUtil
from tweetstake.apps.common.config import Log
from tweetstake.apps.twitter.api import ITwitterApi, ITweet
from tweetstake.apps.twitter.dao import TwitterApiDAO, TweetDAO
from tweetstake.apps.twitter.domain import Tweet, TwitterAccount, AccountsManager


@singleton
class TwitterApiService(ITwitterApi):

    def __get_twitter_api(self, accounts_manager: AccountsManager) -> API:
        twitter_api: API
        authentication: OAuthHandler
        current_account: TwitterAccount

        current_account = accounts_manager.get_current_account()
        authentication = tweepy.OAuthHandler(current_account.consumer_key, current_account.consumer_secret)
        authentication.set_access_token(current_account.token_key, current_account.token_secret)
        twitter_api = tweepy.API(authentication)

        return twitter_api

    def get_tweets_by_criteria_list(self, criteria_list: List[str], accounts_manager: AccountsManager) -> List[Tweet]:
        tweets_all_list: List[Tweet] = list()
        twitter_api: API
        result: List[Tweet] = list()
        index: int = 0
        twice_consecutively_change_account: bool = False

        twitter_api = self.__get_twitter_api(accounts_manager)

        if not accounts_manager.current_account_username:
            accounts_manager.current_account_username = TwitterApiDAO().get_username(twitter_api)
        Log.logger.info(Constants.MSG_CURRENT_ACCOUNT_USERNAME + accounts_manager.current_account_username)

        while index < len(criteria_list):
            try:
                result = TwitterApiDAO().get_tweets_by_criteria(criteria_list[index], twitter_api)
                index += 1
                twice_consecutively_change_account = False
                tweets_all_list = tweets_all_list + result
            except RateLimitError:
                Log.logger.info(Constants.MSG_EXCEEDED_TWITTER_RATE_LIMIT)
                result.clear()
                if twice_consecutively_change_account:
                    accounts_manager.current_account_username = None
                    raise ExceededRateLimitRepeatedly()

                else:
                    self.__change_account(accounts_manager)
                    twitter_api = self.__get_twitter_api(accounts_manager)
                    accounts_manager.current_account_username = TwitterApiDAO().get_username(twitter_api)
                    twice_consecutively_change_account = True

        return tweets_all_list

    def __validate_account_index(self, accounts_manager: AccountsManager) -> None:
        accounts_list_length: int = len(accounts_manager.accounts_list)

        if accounts_list_length == 0:
            raise InfoException(Constants.MSG_EXCEPTION_NO_ACCOUNTS)
        if accounts_manager.current_account_index >= accounts_list_length or accounts_manager.current_account_index < 0:
            raise InfoException(Constants.MSG_EXCEPTION_ACCOUNT_INDEX_OUT_OF_RANGE)

    def __change_account(self, accounts_manager: AccountsManager) -> None:
        self.__validate_account_index(accounts_manager)
        if accounts_manager.current_account_index == len(accounts_manager.accounts_list)-1:
            accounts_manager.current_account_index = 0
        else:
            accounts_manager.current_account_index += 1
        Log.logger.info(Constants.MSG_ACCOUNT_RELIEVED)


@singleton
class TweetService(ITweet):

    def insert_tweet(self, tweet: Tweet) -> None:
        TweetDAO().insert_tweet(tweet)

    def insert_tweets_list(self, tweets_list: List[Tweet]) -> None:
        for tweet in tweets_list:
            TweetDAO().insert_tweet(tweet)

    def get_tweets_count(self) -> int:
        return TweetDAO().get_tweets_count()
