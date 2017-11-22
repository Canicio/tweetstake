from abc import ABCMeta, abstractmethod
from typing import List
from tweetstake.apps.twitter.domain import Tweet, AccountsManager


class ITwitterApi(metaclass=ABCMeta):

    @abstractmethod
    def get_tweets_by_criteria_list(self, criteria_list: List[str], accounts_manager: AccountsManager) -> List[Tweet]:
        """
        Get a list of tweets using a list of search criteria
        :param criteria_list: list of search criteria
        :param accounts_manager: accounts
        :return: list of tweets
        """


class ITweet(metaclass=ABCMeta):

    @abstractmethod
    def insert_tweet(self, tweet: Tweet) -> None:
        """
        Insert tweet in the database
        :param tweet: tweet to insert
        :return: None
        """

    @abstractmethod
    def insert_tweets_list(self, tweets_list: List[Tweet]) -> None:
        """
        Insert tweet list in the database
        :param tweets_list: tweet list to insert
        :return: None
        """

    @abstractmethod
    def get_tweets_count(self) -> int:
        """
        Get an count of the tweets inserted in the database
        :return: count of the tweets inserted
        """
