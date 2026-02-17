import os
import argparse
import sys

# Allow local module imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.email_utils import extract_username, extract_domain, is_valid_email
from core.domain import domain_has_mx
from core.gravatar import gravatar_lookup
from modules.social_accounts import find_social_accounts
from modules.dev_plateforms import find_dev_accounts
from modules.forums import find_forum_accounts


def print_accounts(title: str, accounts: dict) -> None:
    print(f"\n{title}:")
    if accounts:
        for site, url in accounts.items():
            print(f"{site}: {url}")
    else:
        print("None found")


def main(email: str) -> None:
    if not is_valid_email(email):
        raise ValueError("Invalid email format. Example: email@example.com")

    # Parse email data
    username = extract_username(email)
    domain = extract_domain(email)

    print("\nEMAIL:", email)
    print("USERNAME:", username)
    print("DOMAIN ACTIVE:", domain_has_mx(domain))

    # Gravatar check
    avatar = gravatar_lookup(email)
    print("GRAVATAR:", avatar if avatar else "None")

    # Accounts discovery by category
    print_accounts("FOUND SOCIAL ACCOUNTS", find_social_accounts(username))
    print_accounts("FOUND DEV PLATFORM ACCOUNTS", find_dev_accounts(username))
    print_accounts("FOUND FORUM ACCOUNTS", find_forum_accounts(username))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="True-Osint: discover traces associated with an email."
    )
    parser.add_argument("email", help="Target email address (example: email@example.com)")
    return parser.parse_args()


# Script entry point
if __name__ == "__main__":
    args = parse_args()
    try:
        main(args.email)
    except ValueError as exc:
        print(f"Error: {exc}")
        sys.exit(1)
