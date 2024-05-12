import html

from bs4 import BeautifulSoup


def parse_content(content: str) -> str:
    # Unescape the unicode characters
    content = html.unescape(content)

    # Parse the HTML and extract the text
    soup = BeautifulSoup(content, "html.parser")
    plain_text = soup.get_text()

    return plain_text


def parse_post_id(id: str) -> str:
    return id.split("/")[-1]
