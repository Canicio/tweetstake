import unittest
import tweepy
from typing import List
from unittest import mock
from unittest.mock import Mock
from tweetstake.apps.common.util import InfoException
from tweetstake.apps.twitter.domain import AccountsManager, TwitterAccount, Tweet
from tweetstake.apps.twitter.service import TwitterApiService, TweetService


class TwitterApiServiceTest(unittest.TestCase):

    def setUp(self) -> None:

        # Instantiate test class
        self.twitter_api_service: TwitterApiService = TwitterApiService()

        # Input arguments to methods
        self.only_value_criteria_list: List[str] = TestHelper.get_only_value_criteria_list()
        self.several_values_criteria_list: List[str] = TestHelper.get_several_values_criteria_list()
        self.only_account_manager: AccountsManager = TestHelper.get_only_account_manager()
        self.two_accounts_manager: AccountsManager = TestHelper.get_two_accounts_manager()
        self.empty_accounts_manager: AccountsManager = TestHelper.get_empty_accounts_manager()

    @mock.patch('tweetstake.apps.twitter.service.TwitterApiService._TwitterApiService__change_account')
    @mock.patch('tweetstake.apps.twitter.service.TwitterApiService._TwitterApiService__get_twitter_api')
    @mock.patch('tweetstake.apps.twitter.dao.TwitterApiDAO.get_username')
    @mock.patch('tweetstake.apps.twitter.dao.TwitterApiDAO.get_tweets_by_criteria')
    def test_get_tweets_by_criteria_list_by_only_value_criteria_list(self, mocked_get_tweets_by_criteria_method: Mock,
                                                                     mocked_get_username_method: Mock,
                                                                     mocked_get_twitter_api_method: Mock,
                                                                     mocked_change_account_method: Mock) -> None:
        result: List[Tweet]

        # Mock DAO methods
        mocked_get_tweets_by_criteria_method.return_value = TestHelper.get_tweets_three_list()
        mocked_get_username_method.return_value = TestHelper.get_account_username()

        # Mock PRIVATE methods
        mocked_get_twitter_api_method.return_value = tweepy.API()

        # Asserts
        result = self.twitter_api_service.get_tweets_by_criteria_list(criteria_list=self.only_value_criteria_list,
                                                                      accounts_manager=self.only_account_manager)
        mocked_get_twitter_api_method.assert_called_once()
        mocked_change_account_method.assert_not_called()
        mocked_get_tweets_by_criteria_method.assert_called_once()
        self.assertEqual(3, len(result))

    @mock.patch('tweetstake.apps.twitter.service.TwitterApiService._TwitterApiService__change_account')
    @mock.patch('tweetstake.apps.twitter.service.TwitterApiService._TwitterApiService__get_twitter_api')
    @mock.patch('tweetstake.apps.twitter.dao.TwitterApiDAO.get_username')
    @mock.patch('tweetstake.apps.twitter.dao.TwitterApiDAO.get_tweets_by_criteria')
    def test_get_tweets_by_criteria_list_by_several_values_criteria_list(self, mocked_get_tweets_by_criteria_method: Mock,
                                                                         mocked_get_username_method: Mock,
                                                                         mocked_get_twitter_api_method: Mock,
                                                                         mocked_change_account_method: Mock) -> None:
        result: List[Tweet]

        # Mock DAO methods
        mocked_get_tweets_by_criteria_method.return_value = TestHelper.get_tweets_three_list()
        mocked_get_username_method.return_value = TestHelper.get_account_username()

        # Mock PRIVATE methods
        mocked_get_twitter_api_method.return_value = tweepy.API()

        # Asserts
        result = self.twitter_api_service.get_tweets_by_criteria_list(criteria_list=self.several_values_criteria_list,
                                                                      accounts_manager=self.only_account_manager)
        mocked_get_twitter_api_method.assert_called_once()
        mocked_change_account_method.assert_not_called()
        mocked_get_tweets_by_criteria_method.assert_called()
        self.assertEqual(6, len(result))

    def test_validate_account_index_by_empty_accounts_manager(self):
        with self.assertRaises(InfoException):
            self.twitter_api_service._TwitterApiService__validate_account_index(self.empty_accounts_manager)

    def test_validate_account_index_by_index_out_range_accounts_manager(self):
        self.two_accounts_manager.current_account_index = 2
        with self.assertRaises(InfoException):
            self.twitter_api_service._TwitterApiService__validate_account_index(self.two_accounts_manager)

    def test_validate_account_index_by_negative_index_accounts_manager(self):
        self.two_accounts_manager.current_account_index = -1
        with self.assertRaises(InfoException):
            self.twitter_api_service._TwitterApiService__validate_account_index(self.two_accounts_manager)

    @mock.patch('tweetstake.apps.twitter.service.TwitterApiService._TwitterApiService__validate_account_index')
    def test_change_account_by_only_account_manager(self, mocked_validate_account_index_method: Mock):

        # Mock PRIVATE methods
        mocked_validate_account_index_method.return_value = None

        # Asserts
        self.twitter_api_service._TwitterApiService__change_account(self.only_account_manager)
        self.assertEqual(0, self.two_accounts_manager.current_account_index)
        self.twitter_api_service._TwitterApiService__change_account(self.only_account_manager)
        self.assertEqual(0, self.two_accounts_manager.current_account_index)
        mocked_validate_account_index_method.assert_called()


    @mock.patch('tweetstake.apps.twitter.service.TwitterApiService._TwitterApiService__validate_account_index')
    def test_change_account_by_two_accounts_manager(self, mocked_validate_account_index_method: Mock):

        # Mock PRIVATE methods
        mocked_validate_account_index_method.return_value = None

        # Asserts
        self.twitter_api_service._TwitterApiService__change_account(self.two_accounts_manager)
        self.assertEqual(1, self.two_accounts_manager.current_account_index)
        self.twitter_api_service._TwitterApiService__change_account(self.two_accounts_manager)
        self.assertEqual(0, self.two_accounts_manager.current_account_index)
        mocked_validate_account_index_method.assert_called()


class TweetServiceTest(unittest.TestCase):

    def setUp(self) -> None:

        # Instantiate test class
        self.tweet_service: TweetService = TweetService()

        # Input arguments to methods
        self.one_tweet = TestHelper.get_one_tweet()
        self.tweets_three_list = TestHelper.get_tweets_three_list()

    @mock.patch('tweetstake.apps.twitter.dao.TweetDAO.insert_tweet')
    def test_insert_tweet(self, mocked_insert_tweet_method: Mock) -> None:

        # Mock DAO methods
        mocked_insert_tweet_method.return_value = None

        # Asserts
        self.tweet_service.insert_tweet(self.one_tweet)
        mocked_insert_tweet_method.assert_called_once()

    @mock.patch('tweetstake.apps.twitter.dao.TweetDAO.insert_tweet')
    def test_insert_tweets_list(self, mocked_insert_tweet_method: Mock) -> None:

        # Mock DAO methods
        mocked_insert_tweet_method.return_value = None

        # Asserts
        self.tweet_service.insert_tweets_list(self.tweets_three_list)
        mocked_insert_tweet_method.assert_called()

    @mock.patch('tweetstake.apps.twitter.dao.TweetDAO.get_tweets_count')
    def test_get_tweets_count(self, mocked_get_tweets_count_method: Mock) -> None:
        result: int

        # Mock DAO methods
        mocked_get_tweets_count_method.return_value = 3

        # Asserts
        result = self.tweet_service.get_tweets_count()
        self.assertEqual(3, result)
        mocked_get_tweets_count_method.assert_called_once()


class TestHelper(object):

    @staticmethod
    def get_one_tweet() -> Tweet:
        tweet: Tweet = Tweet()
        tweet.id = 1

        return tweet

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

    @staticmethod
    def get_account_username() -> str:
        return "anonymous"

    @staticmethod
    def get_twitter_account1() -> TwitterAccount:
        twitter_account: TwitterAccount = TwitterAccount()

        twitter_account.consumer_key = 'mGo8uIB6wg6nKvWfmBuSjmAv'
        twitter_account.consumer_secret = 'qx4yTUiav6dJvikWo1VvxSORyrRHApUMPldrZrHcAmTg6AXl6U'
        twitter_account.token_key = '130047078134098689-HIaRbONsdhhZc6C9q8n9NWDvYG94aVJ'
        twitter_account.token_secret = 'eQ7Oj3dbutbxc69EPSXFzMvPpjy1Bl01RdiJ6WzzQSIma'

        return twitter_account

    @staticmethod
    def get_twitter_account2() -> TwitterAccount:
        twitter_account: TwitterAccount = TwitterAccount()

        twitter_account.consumer_key = 'yRo8uIB6wg6nKvWfmBuSjmEr'
        twitter_account.consumer_secret = 'wv6yTUiav6dJvikWo1VvxSORyrRHApUMPldrZrHcAmTg6AXk4T'
        twitter_account.token_key = '911047078134098689-HIaRbONsdhhZc6C9q8n9NWDvYG94hBG'
        twitter_account.token_secret = 'zV9Oj3dbutbxc69EPSXFzMvPpjy1Bl01RdiJ6WzzOSRmc'

        return twitter_account

    @staticmethod
    def get_only_account_manager() -> AccountsManager:
        only_account_manager: AccountsManager = AccountsManager()

        only_account_manager.accounts_list = [TestHelper.get_twitter_account1()]

        return only_account_manager

    @staticmethod
    def get_two_accounts_manager() -> AccountsManager:
        many_accounts_manager: AccountsManager = AccountsManager()

        many_accounts_manager.accounts_list = [TestHelper.get_twitter_account1(), TestHelper.get_twitter_account2()]

        return many_accounts_manager

    @staticmethod
    def get_empty_accounts_manager() -> AccountsManager:
        empty_accounts_manager: AccountsManager = AccountsManager()

        empty_accounts_manager.accounts_list = []

        return empty_accounts_manager

    @staticmethod
    def get_only_value_criteria_list() -> List[str]:
        return ['#FelizLunes']

    @staticmethod
    def get_several_values_criteria_list() -> List[str]:
        return ['#FelizLunes', '#Foro']
