import secrets
from urllib.parse import urlparse


_ALPHABET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


def generate_code(length: int = 6) -> str:
    return "".join(secrets.choice(_ALPHABET) for _ in range(length))


def is_valid_url(url: str) -> bool:
    try:
        parsed = urlparse(url)
    except ValueError:
        return False

    return parsed.scheme.lower() in {"http", "https"} and bool(parsed.hostname)
