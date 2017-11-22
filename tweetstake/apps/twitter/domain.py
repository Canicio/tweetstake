from typing import List
from mongoengine import LongField, DynamicDocument


class Tweet(DynamicDocument):
    id = LongField(primary_key=True)


class TwitterAccount(object):

    def __init__(self) -> None:
        self.consumer_key: str = None
        self.consumer_secret: str = None
        self.token_key: str = None
        self.token_secret: str = None


class AccountsManager(object):

    def __init__(self) -> None:
        self.accounts_list: List[TwitterAccount] = None
        self.current_account_index: int = 0
        self.current_account_username: str = None

    def get_current_account(self) -> TwitterAccount:
        return self.accounts_list[self.current_account_index]
