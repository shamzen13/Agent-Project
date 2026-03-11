
# cleans raw text from articles - strips html, normalizes whitespaces and removes junk

import re
from html.parser import HTMLParser

class HTMLStripper(HTMLParser):
    """ html tag stripper"""

    def __init__(self):
        super().__init__()
        self.reset()
        self.fed = []

    def handle_data(self,d):
        self.fed.append(d)

    def get_data(self):
        return " ".join(self.fed)
    

def strip_html(text:str) -> str:
    """ remove html tags from strings"""

    if not text:
        return ""

    stripper = HTMLStripper()
    stripper.feed(text)
    return stripper.get_data()


def clean_text(text:str) -> str:
    """
    Full cleaning pipeline:
    1. Strip HTML tags
    2. Remove URLs
    3. Collapse whitespace
    4. Strip leading/trailing space
    """

    if not text:
        return ""
    
    text = strip_html(text)
    
    text = re.sub(r"http\S+|www.\.S+", "", text)

    text = re.sub(r"\w\s.,!?;:'\"-]", " ", text)

    text = re.sub(r"\s+", " ", text)

    return text.strip()


def truncate(text: str, max_chars: int = 2000) -> str:
    """truncate txt to max char lenghth, ending at word boundary"""

    if len(text) <= max_chars:
        return text
    
    truncated = text[:max_chars]
    last_space = truncated.rfind(" ")
    return truncated[:last_space] + "..."


