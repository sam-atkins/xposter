from abc import ABC, abstractmethod

import requests
from atproto import Client, client_utils


class AbstractClient(ABC):
    """
    Abstract HTTP client
    """

    def __init__(self):
        pass

    @abstractmethod
    def get(self) -> dict:
        pass

    @abstractmethod
    def post(self):
        pass


class MastodonClient(AbstractClient):
    """
    Mastodon HTTP client
    """

    def __init__(self, host: str, user: str):
        self.host = host
        self.user = user

    def get(self) -> dict:
        url = f"{self.host}/users/{self.user}/outbox?page=true"
        response = requests.get(url)
        return response.json()

    def post(self):
        raise NotImplementedError


class BlueskyClient(AbstractClient):
    """
    Bluesky HTTP client
    """

    def __init__(self, handle: str, password: str):
        self.handle = handle
        self.password = password

    def get(self) -> dict:
        raise NotImplementedError

    def post(self, content: client_utils.TextBuilder):
        client = Client()
        client.login(self.handle, self.password)
        client.send_post(text=content)
