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
REQUEST_TIMEOUT = 10

USERNAME_SITES = {
    "GitHub": "https://github.com/{}",
    "GitLab": "https://gitlab.com/{}",
    "Bitbucket": "https://bitbucket.org/{}",
    "Reddit": "https://www.reddit.com/user/{}",
    "Medium": "https://medium.com/@{}",
}

NOT_FOUND_MARKERS = {
    "GitHub": ("not found", "page not found"),
    "GitLab": ("not found", "404"),
    "Bitbucket": ("page not found",),
    "Reddit": ("sorry, nobody on reddit goes by that name",),
    "Medium": ("page not found",),
}

CONFIDENCE_SCORE = {"high": 3, "medium": 2, "low": 1}


def _http_get(url, params=None, json_accept=False):
    headers = dict(HEADERS)
    if json_accept:
        headers["Accept"] = "application/vnd.github+json"
    try:
        return requests.get(url, params=params, headers=headers, timeout=REQUEST_TIMEOUT)
    except requests.RequestException:
        return None


def _profile_mentions_email(profile_url, email):
    response = _http_get(profile_url)
    if response is None:
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
    response = _http_get(
        f"{GITHUB_API}/search/users",
        params={"q": f"\"{email}\" in:email", "per_page": 10},
        json_accept=True,
    )
    if response is None or response.status_code != 200:
        return found

    try:
        items = response.json().get("items", [])
    except ValueError:
        return found

    for item in items:
        login = item.get("login")
        if not login:
            continue

        user_response = _http_get(f"{GITHUB_API}/users/{login}", json_accept=True)
        if user_response is None or user_response.status_code != 200:
            continue
        try:
            user = user_response.json()
        except ValueError:
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
    response = _http_get(
        f"{GITHUB_API}/search/commits",
        params={"q": f"author-email:{email}", "per_page": 20},
        json_accept=True,
    )
    if response is None or response.status_code != 200:
        return found

    try:
        commits = response.json().get("items", [])
    except ValueError:
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


def _extract_username_based_accounts(username):
    """
    Fallback when no direct public email evidence exists.
    Returns possible accounts based on local-part username match.
    """
    found = []
    username_lower = username.lower()

    for site, url_template in USERNAME_SITES.items():
        candidate_url = url_template.format(username)
        response = _http_get(candidate_url)
        if response is None or response.status_code != 200:
            continue

        page_content = response.text.lower()
        markers = NOT_FOUND_MARKERS.get(site, ())
        if any(marker in page_content for marker in markers):
            continue

        resolved_url = response.url or candidate_url
        # If redirect lands on a generic page without username, discard it.
        if username_lower not in resolved_url.lower() and username_lower not in page_content[:5000]:
            continue
        if "login" in resolved_url.lower() or "signup" in resolved_url.lower():
            continue

        found.append(
            {
                "site": site,
                "url": resolved_url,
                "source": "Username match from email local-part",
                "confidence": "low",
            }
        )
    return found


def _dedupe_accounts(accounts):
    by_url = {}
    for account in accounts:
        url = account["url"]
        existing = by_url.get(url)
        if not existing:
            by_url[url] = account
            continue

        current_score = CONFIDENCE_SCORE.get(account.get("confidence", "low"), 1)
        existing_score = CONFIDENCE_SCORE.get(existing.get("confidence", "low"), 1)
        if current_score > existing_score:
            by_url[url] = account

    return sorted(
        by_url.values(),
        key=lambda item: CONFIDENCE_SCORE.get(item.get("confidence", "low"), 1),
        reverse=True,
    )


def find_social_accounts(email, include_probable=True):
    username = extract_username(email).strip()
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

    if include_probable:
        discovered_accounts.extend(_extract_username_based_accounts(username))

    return _dedupe_accounts(discovered_accounts)
