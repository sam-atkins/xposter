import pytest

from src.bsky import Bluesky
from src.http import AbstractClient


class MockBskyClient(AbstractClient):
    def __init__(self):
        pass

    def get(self):
        pass

    def post(self):
        pass


@pytest.fixture
def client():
    return MockBskyClient


def test__build_rich_text_with_tags(client):
    mock_client = client()
    bsky = Bluesky(mock_client)
    content = "St. Pauli promoted to the #bundesliga #stpauli"
    result = bsky._build_rich_text(content)
    assert result.build_text() == "St. Pauli promoted to the #bundesliga #stpauli"


def test_build_rich_text_with_link(client):
    mock_client = client()
    bsky = Bluesky(mock_client)
    content = "Recommended read: Kylian Mbappe: The incredible, inevitable rise of a superstar as he leaves PSG ($ paywall) https://theathletic.com/5484970/2024/05/10/kylian-mbappe-psg-real-madrid-france/ #Football #Mbappe"
    result = bsky._build_rich_text(content)
    assert (
        result.build_text()
        == "Recommended read: Kylian Mbappe: The incredible, inevitable rise of a superstar as he leaves PSG ($ paywall) https://theathletic.com/5484970/2024/05/10/kylian-mbappe-psg-real-madrid-france/ #Football #Mbappe"
    )
