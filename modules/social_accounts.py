import requests
from core.email_utils import extract_username
from core.gravatar import gravatar_profile_lookup

SOCIAL_SITES = {
    "GitHub": "https://github.com/{}",
    "Twitter": "https://twitter.com/{}",
    "Instagram": "https://www.instagram.com/{}",
    "Facebook": "https://www.facebook.com/{}",
    "Reddit": "https://www.reddit.com/user/{}",
    "Medium": "https://medium.com/@{}"
}

HEADERS = {"User-Agent": "True-Osint/1.0 (educational use)"}


def _profile_mentions_email(profile_url, email):
    try:
        response = requests.get(profile_url, headers=HEADERS, timeout=8)
    except requests.RequestException:
        return False, None

    if response.status_code != 200:
        return False, None

    page_content = response.text.lower()
    return email.lower() in page_content, response.url


def _extract_gravatar_accounts(email):
    profile = gravatar_profile_lookup(email)
    if not profile:
        return []

    found = []
    for account in profile.get("accounts", []):
        site_name = account.get("shortname") or account.get("domain") or account.get("name")
        account_url = account.get("url")
        if site_name and account_url:
            found.append(
                {
                    "site": site_name.capitalize(),
                    "url": account_url,
                    "source": "Gravatar profile",
                    "confidence": "high",
                }
            )
    return found


def find_social_accounts(email):
    username = extract_username(email)
    discovered_accounts = []

    # High-confidence accounts explicitly linked in Gravatar profile
    discovered_accounts.extend(_extract_gravatar_accounts(email))

    # Medium-confidence accounts where profile page publicly contains exact email
    for site, url_template in SOCIAL_SITES.items():
        candidate_url = url_template.format(username)
        has_email, resolved_url = _profile_mentions_email(candidate_url, email)
        if has_email:
            discovered_accounts.append(
                {
                    "site": site,
                    "url": resolved_url or candidate_url,
                    "source": "Public profile contains email",
                    "confidence": "medium",
                }
            )

    # Deduplicate by URL while preserving order
    deduped = []
    seen_urls = set()
    for account in discovered_accounts:
        url = account["url"]
        if url in seen_urls:
            continue
        seen_urls.add(url)
        deduped.append(account)
    return deduped
