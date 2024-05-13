import json
import tempfile

import pytest

from src.http import AbstractClient
from src.mastodon import Mastodon
from tests.data.outbox import MASTODON_OUTBOX


class MockMastodonClient(AbstractClient):
    def __init__(self):
        pass

    def get(self):
        return MASTODON_OUTBOX

    def post(self, posts: list[dict]):
        pass


@pytest.fixture
def client():
    return MockMastodonClient


def test_get_posts_to_cross_post(client):
    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as tmp:
        with open("tests/data/mstd.json") as f:
            data = json.load(f)

        json.dump(data, tmp)

    mock_client = client()
    mstd = Mastodon(mock_client, tmp.name)

    result = mstd.get_posts_to_cross_post()
    assert result == [
        {
            "id": "112418369440902630",
            "content": "Flick back to #FCBayern? Not sure what to make of this. Incredible achievement with the treble. Chances of reaching those heights again? https://theathletic.com/5479047/2024/05/10/bayern-munich-next-manager-hansi-flick-talks/",
            "timestamp": "2024-05-10T19:09:46Z",
        }
    ]

    # assert our db file has been updated
    with open(tmp.name) as f:
        data = json.load(f)
        assert data == {
            "112009704278934987": {
                "content": "Very excited about uv: Python packaging in Rust. From the makers of #ruff . One to watch #python #rustlang https://astral.sh/blog/uv",
                "timestamp": "2024-02-28T15:00:50Z",
            },
            "112376953414912830": {
                "content": "Big day for Ipswich Town tomorrow. Only 1 point needed and we’re promoted. Back in the Premier League after 22 years? 🤞 #itfc",
                "timestamp": "2024-05-03T11:37:07Z",
            },
            "112417922089702206": {
                "content": "The weekend has arrived 😎🍺",
                "timestamp": "2024-05-10T17:16:00Z",
            },
            "112418129743774124": {
                "content": "The more I read about the Jack Dorsey and Bluesky thing, the more I think #bluesky is better off without him. But what do I know",
                "timestamp": "2024-05-10T18:08:48Z",
            },
            "112418369440902630": {
                "content": "Flick back to #FCBayern? Not sure what to make of this. Incredible achievement with the treble. Chances of reaching those heights again? https://theathletic.com/5479047/2024/05/10/bayern-munich-next-manager-hansi-flick-talks/",
                "timestamp": "2024-05-10T19:09:46Z",
            },
        }


def test_get_mastodon_posts(client):
    mock_client = client()
    mstd = Mastodon(mock_client, "tmp_file")

    outbox = mstd._get_raw_posts()
    assert outbox is not None
    assert len(outbox) == 6


def test_get_content(client):
    mock_client = client()
    mstd = Mastodon(mock_client, "tmp_file")

    result = mstd._get_content()
    assert len(result) == 5
    assert result == [
        {
            "id": "112009704278934987",
            "content": "Very excited about uv: Python packaging in Rust. From the makers of #ruff . One to watch #python #rustlang https://astral.sh/blog/uv",
            "timestamp": "2024-02-28T15:00:50Z",
        },
        {
            "id": "112376953414912830",
            "content": "Big day for Ipswich Town tomorrow. Only 1 point needed and we’re promoted. Back in the Premier League after 22 years? 🤞 #itfc",
            "timestamp": "2024-05-03T11:37:07Z",
        },
        {
            "id": "112417922089702206",
            "content": "The weekend has arrived 😎🍺",
            "timestamp": "2024-05-10T17:16:00Z",
        },
        {
            "id": "112418129743774124",
            "content": "The more I read about the Jack Dorsey and Bluesky thing, the more I think #bluesky is better off without him. But what do I know",
            "timestamp": "2024-05-10T18:08:48Z",
        },
        {
            "id": "112418369440902630",
            "content": "Flick back to #FCBayern? Not sure what to make of this. Incredible achievement with the treble. Chances of reaching those heights again? https://theathletic.com/5479047/2024/05/10/bayern-munich-next-manager-hansi-flick-talks/",
            "timestamp": "2024-05-10T19:09:46Z",
        },
    ]
