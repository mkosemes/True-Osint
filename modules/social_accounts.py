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
GITHUB_API = "https://api.github.com"


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


def _extract_github_public_email_accounts(email):
    """
    Search GitHub users by email and keep only exact public-email matches.
    This is a high-confidence signal because the profile exposes this email.
    """
    found = []
    try:
        response = requests.get(
            f"{GITHUB_API}/search/users",
            params={"q": f"\"{email}\" in:email", "per_page": 10},
            headers=HEADERS | {"Accept": "application/vnd.github+json"},
            timeout=10,
        )
        if response.status_code != 200:
            return found
        items = response.json().get("items", [])
    except (requests.RequestException, ValueError):
        return found

    for item in items:
        login = item.get("login")
        if not login:
            continue
        try:
            user_response = requests.get(
                f"{GITHUB_API}/users/{login}",
                headers=HEADERS | {"Accept": "application/vnd.github+json"},
                timeout=10,
            )
            if user_response.status_code != 200:
                continue
            user = user_response.json()
        except (requests.RequestException, ValueError):
            continue

        public_email = (user.get("email") or "").strip().lower()
        if public_email != email.lower():
            continue
        found.append(
            {
                "site": "GitHub",
                "url": user.get("html_url") or f"https://github.com/{login}",
                "source": "GitHub public profile email",
                "confidence": "high",
            }
        )
    return found


def _extract_github_commit_accounts(email):
    """
    Search public commits by author email and keep commits where the exact
    author email matches, then map to associated GitHub accounts.
    """
    found = []
    try:
        response = requests.get(
            f"{GITHUB_API}/search/commits",
            params={"q": f"author-email:{email}", "per_page": 20},
            headers=HEADERS | {"Accept": "application/vnd.github+json"},
            timeout=10,
        )
        if response.status_code != 200:
            return found
        commits = response.json().get("items", [])
    except (requests.RequestException, ValueError):
        return found

    seen_logins = set()
    target = email.lower()
    for item in commits:
        commit_author = item.get("commit", {}).get("author", {})
        commit_email = (commit_author.get("email") or "").strip().lower()
        if commit_email != target:
            continue

        author = item.get("author") or {}
        login = author.get("login")
        if not login or login in seen_logins:
            continue
        seen_logins.add(login)
        found.append(
            {
                "site": "GitHub",
                "url": author.get("html_url") or f"https://github.com/{login}",
                "source": "GitHub public commit author email",
                "confidence": "medium",
            }
        )
    return found


def find_social_accounts(email):
    username = extract_username(email)
    discovered_accounts = []

    # High-confidence accounts explicitly linked in Gravatar profile
    discovered_accounts.extend(_extract_gravatar_accounts(email))
    discovered_accounts.extend(_extract_github_public_email_accounts(email))
    discovered_accounts.extend(_extract_github_commit_accounts(email))

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
