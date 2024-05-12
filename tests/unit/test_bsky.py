from src.bsky import _build_rich_text


def test__build_rich_text():
    content = "St. Pauli promoted to the #bundesliga #stpauli"
    result = _build_rich_text(content)
    assert result.build_text() == "St. Pauli promoted to the #bundesliga #stpauli"
