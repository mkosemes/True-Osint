import sys
import os

# Allow local module imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.email_utils import extract_username, extract_domain, is_valid_email
from core.domain import domain_has_mx
from core.gravatar import gravatar_lookup
from modules.social_accounts import find_social_accounts


def main(email):
    if not is_valid_email(email):
        print("Email invalide. Exemple attendu: email@example.com")
        return 1

    # Parse email data
    username = extract_username(email)
    domain = extract_domain(email)

    print("\nEMAIL:", email)
    print("USERNAME:", username)
    print("DOMAIN ACTIVE:", domain_has_mx(domain))

    # Gravatar check
    avatar = gravatar_lookup(email)
    print("GRAVATAR:", avatar if avatar else "None")

    # Social accounts discovery with stronger verification signals
    print("\nFOUND LINKED ACCOUNTS:")
    lookup = find_social_accounts(email, return_details=True)
    accounts = lookup["accounts"]
    diagnostics = lookup["diagnostics"]
    if accounts:
        verified = [a for a in accounts if a.get("confidence") in {"high", "medium"}]
        probable = [a for a in accounts if a.get("confidence") == "low"]

        if verified:
            print("Verified (public evidence):")
            for account in verified:
                print(
                    f"- {account['site']}: {account['url']} "
                    f"(source={account['source']}, confidence={account['confidence']})"
                )

        if probable:
            print("Probable (username match):")
            for account in probable:
                print(
                    f"- {account['site']}: {account['url']} "
                    f"(source={account['source']}, confidence={account['confidence']})"
                )

        if not verified and not probable:
            print("None found")
            print("No public account evidence found for this email.")
    else:
        print("None found")
        print("No public account evidence found for this email.")

    if diagnostics:
        print("\nINFO:")
        for message in diagnostics:
            print(f"- {message}")
    return 0


# Script entry point
if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--web":
        from web_interface import run_server

        run_server()
        sys.exit(0)

    if len(sys.argv) == 2:
        sys.exit(main(sys.argv[1]))

    user_email = input("Entrez une adresse email: ").strip()
    sys.exit(main(user_email))
