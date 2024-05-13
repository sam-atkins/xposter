import json

from src.http import AbstractClient
from src.parsers import parse_content, parse_post_id


class Mastodon:
    def __init__(self, client: AbstractClient, mastodon_data_file: str):
        self.client = client
        self.mastodon_data_file = mastodon_data_file

    def get_posts_to_cross_post(self) -> list[dict]:
        posts = []
        data = self._get_mstd_data(self.mastodon_data_file)
        for content_object in self._get_content():
            id = content_object.get("id")
            hit = data.get(id)
            # if the id is in the db it was already cross-posted
            if hit:
                continue
            posts.append(content_object)
            self._write_mstd_data(content_object, self.mastodon_data_file)

        return posts

    def _get_content(self) -> list[dict]:
        parsed_content = []
        raw_posts = self._get_raw_posts()
        for content_object in raw_posts:
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

    def _get_raw_posts(self) -> list[dict]:
        outbox = self._get_outbox()
        ordered_items = outbox.get("orderedItems", {})

        raw_posts = []
        for item in ordered_items:
            if item.get("type") == "Create":
                raw_posts.append(item.get("object"))

        return raw_posts

    def _get_outbox(self) -> dict:
        return self.client.get()

    def _get_mstd_data(self, mstd_data_file: str) -> dict:
        with open(mstd_data_file) as f:
            return json.load(f)

    def _write_mstd_data(self, data: dict, mstd_data_file: str):
        with open(mstd_data_file) as f:
            existing_data = json.load(f)

        new_id = data.get("id")
        new_content = data.get("content")
        new_timestamp = data.get("timestamp")
        new_data = {new_id: {"content": new_content, "timestamp": new_timestamp}}
        existing_data.update(new_data)

        with open(mstd_data_file, "w") as f:
            json.dump(existing_data, f, indent=4)
