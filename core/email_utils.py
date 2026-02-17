import re
from typing import Tuple


EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def is_valid_email(email: str) -> bool:
    if not isinstance(email, str):
        return False
    return bool(EMAIL_PATTERN.match(email.strip()))


def normalize_email(email: str) -> str:
    return email.strip().lower()


def split_email(email: str) -> Tuple[str, str]:
    if not is_valid_email(email):
        raise ValueError(f"Invalid email format: {email}")
    username, domain = normalize_email(email).split("@", 1)
    return username, domain


def extract_username(email: str) -> str:
    return split_email(email)[0]


def extract_domain(email: str) -> str:
    return split_email(email)[1]
 