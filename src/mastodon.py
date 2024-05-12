import json
import os

import requests
from dotenv import load_dotenv

from src.parsers import parse_content, parse_post_id

# Load the .env file
load_dotenv()


def get_posts_to_cross_post(
    content_objects: list[dict], mstd_data_file: str
) -> list[dict]:
    posts = []
    data = _get_mstd_data(mstd_data_file)
    for content_object in content_objects:
        id = content_object.get("id")
        hit = data.get(id)
        # if the id is in the db it was already cross-posted
        if hit:
            continue
        posts.append(content_object)
        _write_mstd_data(content_object, mstd_data_file)

    return posts


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


def get_mastodon_posts(outbox: dict) -> list[dict]:
    ordered_items = outbox.get("orderedItems", {})

    raw_posts = []
    for item in ordered_items:
        if item.get("type") == "Create":
            raw_posts.append(item.get("object"))

    return raw_posts


def get_mastodon_outbox() -> dict:
    # TODO handle if env vars not set, as part of config mgmt
    mastodon_url = os.getenv("MASTODON_HOST")
    mastodon_user = os.getenv("MASTODON_USER")

    mastodon_url = f"{mastodon_url}/users/{mastodon_user}/outbox?page=true"
    response = requests.get(mastodon_url)

    return response.json()


def _get_mstd_data(mstd_data_file: str) -> dict:
    with open(mstd_data_file) as f:
        return json.load(f)


def _write_mstd_data(data: dict, mstd_data_file: str):
    with open(mstd_data_file) as f:
        existing_data = json.load(f)

    new_id = data.get("id")
    new_content = data.get("content")
    new_timestamp = data.get("timestamp")
    new_data = {new_id: {"content": new_content, "timestamp": new_timestamp}}
    existing_data.update(new_data)

    with open(mstd_data_file, "w") as f:
        json.dump(existing_data, f)
