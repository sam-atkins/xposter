import os

from atproto import Client, client_utils
from dotenv import load_dotenv

load_dotenv()


def post_to_bsky(posts: list[dict]):
    bsky_handle = os.getenv("BLUESKY_HANDLE")
    bsky_password = os.getenv("BLUESKY_PASSWORD")
    client = Client()
    client.login(bsky_handle, bsky_password)

    for post in posts:
        rich_text = _build_rich_text(post["content"])
        client.send_post(text=rich_text)


def _build_rich_text(content: str):
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
