from src.mastodon import get_content, get_mastodon_outbox, get_mastodon_posts


def main():
    outbox = get_mastodon_outbox()
    outbox_objects = get_mastodon_posts(outbox)
    if not outbox_objects:
        return
    parsed_content = get_content(outbox_objects)
    print(parsed_content)


if __name__ == "__main__":
    main()
