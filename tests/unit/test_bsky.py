from src.bsky import _build_rich_text


def test__build_rich_text_with_tags():
    content = "St. Pauli promoted to the #bundesliga #stpauli"
    result = _build_rich_text(content)
    assert result.build_text() == "St. Pauli promoted to the #bundesliga #stpauli"


def test_build_rich_text_with_link():
    content = "Recommended read: Kylian Mbappe: The incredible, inevitable rise of a superstar as he leaves PSG ($ paywall) https://theathletic.com/5484970/2024/05/10/kylian-mbappe-psg-real-madrid-france/ #Football #Mbappe"
    result = _build_rich_text(content)
    assert (
        result.build_text()
        == "Recommended read: Kylian Mbappe: The incredible, inevitable rise of a superstar as he leaves PSG ($ paywall) https://theathletic.com/5484970/2024/05/10/kylian-mbappe-psg-real-madrid-france/ #Football #Mbappe"
    )
