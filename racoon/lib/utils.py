import re


def clean_str(x: str) -> str:
    return re.sub(r'[^\w\s_]+', '', x).strip().replace(" ", "-").lower()
