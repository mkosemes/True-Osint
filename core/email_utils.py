import re


EMAIL_REGEX = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")


def is_valid_email(email):
    return bool(EMAIL_REGEX.match(email.strip()))


def extract_username(email):
    return email.split("@")[0].strip()


def extract_domain(email):
    return email.split("@")[1].strip()

 