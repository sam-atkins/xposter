import os
import sys

from dotenv import load_dotenv

from src.bsky import post_to_bsky
from src.mastodon import (
    get_content,
    get_mastodon_outbox,
    get_mastodon_posts,
    get_posts_to_cross_post,
)

# Load the .env file
load_dotenv()


def main():
    outbox = get_mastodon_outbox()
    outbox_objects = get_mastodon_posts(outbox)
    if not outbox_objects:
        # TODO log the error
        return
    parsed_content = get_content(outbox_objects)
    mstd_data_file = os.getenv("MSTD_DATA_FILE")

    # TODO refactor to handle all config
    if not mstd_data_file:
        sys.exit("MSTD_DATA_FILE not set in .env")

    posts_to_cross_post = get_posts_to_cross_post(parsed_content, mstd_data_file)
    if not posts_to_cross_post:
        print("No posts to cross-post")
        sys.exit()

    print("Posts to cross-post:")
    print(posts_to_cross_post)
    post_to_bsky(posts_to_cross_post)
    print("Cross-posted to Bluesky")


if __name__ == "__main__":
    main()
