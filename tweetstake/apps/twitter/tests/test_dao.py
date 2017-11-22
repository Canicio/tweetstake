import unittest
from typing import List
from unittest import mock
from unittest.mock import Mock
from tweepy import API, OAuthHandler
from tweetstake.apps.twitter.dao import TwitterApiDAO, TweetDAO
from tweetstake.apps.twitter.domain import Tweet


class TwitterApiDAOTest(unittest.TestCase):

    def setUp(self) -> None:

        # Instantiate test class
        self.twitter_api_dao: TwitterApiDAO = TwitterApiDAO()

    @mock.patch('tweetstake.apps.twitter.dao.TwitterApiDAO._TwitterApiDAO__deserialize_tweets_list')
    @mock.patch('tweepy.API.search')
    def test_get_tweets_by_criteria(self, mocked_tweepy_api_search_method: Mock,
                                    mocked_deserialize_tweets_list_method: Mock) -> None:

        result: List[Tweet]

        # Mock TWITTER API methods
        mocked_tweepy_api_search_method.return_value = [None]

        # Mock PRIVATE methods
        mocked_deserialize_tweets_list_method.return_value = TestHelper.get_tweets_three_list()

        # Asserts
        result = self.twitter_api_dao.get_tweets_by_criteria(criteria='test', api=API())
        mocked_tweepy_api_search_method.assert_called_once_with(q='test')
        mocked_deserialize_tweets_list_method.assert_called_once_with([None])
        self.assertEqual(3, len(result))

    @mock.patch('tweepy.OAuthHandler.get_username')
    def test_get_username(self, mocked_tweepy_api_get_username_method: Mock) -> None:

        result: str

        # Mock TWITTER API methods
        mocked_tweepy_api_get_username_method.return_value = 'anonymous'

        # Asserts
        result = self.twitter_api_dao.get_username(API(OAuthHandler(consumer_key='', consumer_secret='')))
        mocked_tweepy_api_get_username_method.assert_called_once()
        self.assertEqual('anonymous', result)


class TweetDAOTest(unittest.TestCase):

    def setUp(self) -> None:

        # Instantiate test class
        self.tweet_dao: TweetDAO = TweetDAO()

    @mock.patch('tweetstake.apps.twitter.domain.Tweet.save')
    def test_insert_tweet(self, mocked_tweet_save_method: Mock) -> None:

        # Mock DOMAIN methods
        mocked_tweet_save_method.return_value = None

        # Asserts
        self.tweet_dao.insert_tweet(Tweet())
        mocked_tweet_save_method.assert_called_once()


class TestHelper(object):

    @staticmethod
    def get_tweets_three_list() -> List[Tweet]:
        tweets_list: List[Tweet] = list()
        tweet1: Tweet = Tweet()
        tweet2: Tweet = Tweet()
        tweet3: Tweet = Tweet()

        tweet1.id = 1
        tweet2.id = 2
        tweet3.id = 3
        tweets_list.append(tweet1)
        tweets_list.append(tweet2)
        tweets_list.append(tweet3)

        return tweets_list
