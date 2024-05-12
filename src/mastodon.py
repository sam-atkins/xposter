import os
from typing import Optional

import requests
from dotenv import load_dotenv
from src.parsers import parse_content, parse_post_id

# Load the .env file
load_dotenv()


def get_content(content_objects: list[dict]):
    parsed_content = []
    for content_object in content_objects:
        reply = content_object.get("inReplyTo")
        if reply:
            continue
        timestamp = content_object.get("published")
        id = content_object.get("id", "")
        post_id = parse_post_id(id)

        content = content_object.get("content")
        if not content:
            continue
        plain_text = parse_content(content)
        parsed_content.append(
            {
                "id": post_id,
                "content": plain_text,
                "timestamp": timestamp,
            }
        )

    # Sort the list of dictionaries by the timestamp, oldest first
    parsed_content = sorted(parsed_content, key=lambda x: x["timestamp"])

    return parsed_content


def get_mastodon_posts(outbox: dict) -> Optional[list[dict]]:
    ordered_items = outbox.get("orderedItems")
    if not ordered_items:
        # TODO log the error
        return

    raw_posts = []
    for item in ordered_items:
        if item.get("type") == "Create":
            raw_posts.append(item.get("object"))

    return raw_posts


def get_mastodon_outbox() -> dict:
    mastodon_url = os.getenv("MASTODON_HOST")
    mastodon_user = os.getenv("MASTODON_USER")
    # TODO handle if env vars not set

    mastodon_url = f"{mastodon_url}/users/{mastodon_user}/outbox?page=true"
    response = requests.get(mastodon_url)

    return response.json()
