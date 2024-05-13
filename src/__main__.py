import sys

from src.bsky import Bluesky
from src.config import load_config
from src.http import BlueskyClient, MastodonClient
from src.mastodon import Mastodon


def main():
    config = load_config()

    mstd_client = MastodonClient(config.mastodon_host, config.mastodon_user)
    mastodon = Mastodon(
        mstd_client,
        config.mastodon_data_file,
    )
    posts_to_cross_post = mastodon.get_posts_to_cross_post()

    if not posts_to_cross_post:
        print("No posts to cross-post")
        sys.exit()

    print("Posts to cross-post:")
    print(posts_to_cross_post)

    bsky_client = BlueskyClient(config.bluesky_handle, config.bluesky_password)
    bluesky = Bluesky(bsky_client)
    bluesky.post(posts_to_cross_post)
    print("Cross-posted to Bluesky")


if __name__ == "__main__":
    main()
