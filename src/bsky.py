from atproto import client_utils

from src.http import BlueskyClient


class Bluesky:
    """
    Responsible for interactions with Bluesky.
    """

    def __init__(self, bluesky_client: BlueskyClient):
        self.client = bluesky_client

    def get(self) -> dict:
        raise NotImplementedError

    def post(self, posts: list[dict]):
        """
        Post to Bluesky.
        """
        for post in posts:
            rich_text = self._build_rich_text(post["content"])
            self.client.post(rich_text)

    def _build_rich_text(self, content: str):
        """
        Build rich text for Bluesky.
        """
        text_builder = client_utils.TextBuilder()
        words = content.split()

        for i, word in enumerate(words):
            if word.startswith("#"):
                tag = word[1:]
                if i == 0:
                    text_builder.tag(f"#{tag}", tag)
                else:
                    text_builder.tag(f" #{tag}", tag)
            elif word.startswith("http"):
                url = word
                if i == 0:
                    text_builder.link(url, url)
                else:
                    text_builder.link(f" {url}", url)
            else:
                if i == 0:
                    text_builder.text(word)
                else:
                    text_builder.text(f" {word}")

        return text_builder
