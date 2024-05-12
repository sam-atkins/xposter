import pytest

from src.parsers import parse_content, parse_post_id


@pytest.mark.parametrize(
    "content, expected",
    [
        (
            '\u003cp\u003eFlick back to \u003ca href="https://hachyderm.io/tags/FCBayern" class="mention hashtag" rel="tag"\u003e#\u003cspan\u003eFCBayern\u003c/span\u003e\u003c/a\u003e? Not sure what to make of this. Incredible achievement with the treble. Chances of reaching those heights again? \u003ca href="https://theathletic.com/5479047/2024/05/10/bayern-munich-next-manager-hansi-flick-talks/" target="_blank" rel="nofollow noopener noreferrer" translate="no"\u003e\u003cspan class="invisible"\u003ehttps://\u003c/span\u003e\u003cspan class="ellipsis"\u003etheathletic.com/5479047/2024/0\u003c/span\u003e\u003cspan class="invisible"\u003e5/10/bayern-munich-next-manager-hansi-flick-talks/\u003c/span\u003e\u003c/a\u003e\u003c/p\u003e',
            "Flick back to #FCBayern? Not sure what to make of this. Incredible achievement with the treble. Chances of reaching those heights again? https://theathletic.com/5479047/2024/05/10/bayern-munich-next-manager-hansi-flick-talks/",
        ),
        (
            '\u003cp\u003eThe more I read about the Jack Dorsey and Bluesky thing, the more I think \u003ca href="https://hachyderm.io/tags/bluesky" class="mention hashtag" rel="tag"\u003e#\u003cspan\u003ebluesky\u003c/span\u003e\u003c/a\u003e is better off without him. But what do I know\u003c/p\u003e',
            "The more I read about the Jack Dorsey and Bluesky thing, the more I think #bluesky is better off without him. But what do I know",
        ),
    ],
)
def test_parsers(content, expected):
    assert parse_content(content) == expected


@pytest.mark.parametrize(
    "id, expected",
    [
        (
            "https://hachyderm.io/users/samatkins/statuses/112418369440902630",
            "112418369440902630",
        ),
        (
            "https://hachyderm.io/users/samatkins/statuses/112417922089702206",
            "112417922089702206",
        ),
    ],
)
def test_parse_post_id(id, expected):
    assert parse_post_id(id) == expected
