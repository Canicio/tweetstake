import pytz
from abc import ABCMeta, abstractmethod
from datetime import datetime
from typing import List
from tweepy import API
from tweepy.models import Status
from tweetstake.apps.common.decorators import singleton
from tweetstake.apps.common.util import Constants
from tweetstake.apps.twitter.domain import Tweet


class ITwitterApiDAO(metaclass=ABCMeta):

    @abstractmethod
    def get_tweets_by_criteria(self, criteria: str, api: API) -> List[Tweet]:
        """
        Get a list of tweets using a search criteria
        :param criteria: search criteria
        :param api: tweepy object to use twitter api
        :return:
        """

    @abstractmethod
    def get_username(self, api: API) -> str:
        """
        Get username of current account
        :param api: tweepy object to use twitter api
        :return: username
        """


class ITweetDAO(metaclass=ABCMeta):

    @abstractmethod
    def insert_tweet(self, tweet: Tweet) -> None:
        """
        Insert tweet in the database
        :param tweet: tweet to insert
        :return: None
        """

    @abstractmethod
    def get_tweets_count(self) -> int:
        """
        Get an count of the tweets inserted in the database
        :return: count of the tweets inserted
        """


@singleton
class TwitterApiDAO(ITwitterApiDAO):

    def get_tweets_by_criteria(self, criteria: str, api: API) -> List[Tweet]:
        gross_tweets_list: List[Status]
        result_list: List[Tweet]

        gross_tweets_list = api.search(q=criteria)
        result_list = self.__deserialize_tweets_list(gross_tweets_list)

        return result_list

    def get_username(self, api: API) -> str:
        return api.auth.get_username()

    def __deserialize_tweets_list(self, gross_tweets_list: List[Status]) -> List[Tweet]:
        tweets_list: List[Tweet] = list()
        tweet: Tweet

        for item in gross_tweets_list:
            tweet = Tweet(**item._json)
            tweet.created_at = datetime.strptime(tweet.created_at, Constants.FORMAT_DESERIALIZE_TWEET_DATETIME).replace(tzinfo=pytz.UTC)
            tweet.user['created_at'] = datetime.strptime(tweet.user['created_at'], Constants.FORMAT_DESERIALIZE_TWEET_DATETIME).replace(tzinfo=pytz.UTC)
            tweets_list.append(tweet)

        return tweets_list


@singleton
class TweetDAO(ITweetDAO):

    def insert_tweet(self, tweet: Tweet) -> None:
        tweet.save()

    def get_tweets_count(self) -> int:
        return Tweet.objects().count()
