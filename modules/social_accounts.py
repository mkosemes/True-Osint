import re

import requests

from core.email_utils import extract_username
from core.gravatar import gravatar_profile_lookup

EMAIL_SCAN_SITES = {
    "GitHub": "https://github.com/{}",
    "Reddit": "https://www.reddit.com/user/{}",
    "Medium": "https://medium.com/@{}",
}

USERNAME_SITES = {
    "GitHub": "https://github.com/{}",
    "GitLab": "https://gitlab.com/{}",
    "Bitbucket": "https://bitbucket.org/{}",
    "Reddit": "https://www.reddit.com/user/{}",
    "Medium": "https://medium.com/@{}",
    "Dev.to": "https://dev.to/{}",
    "Keybase": "https://keybase.io/{}",
    "Kaggle": "https://www.kaggle.com/{}",
}

NOT_FOUND_MARKERS = {
    "GitHub": ("not found", "page not found"),
    "GitLab": ("not found", "404"),
    "Bitbucket": ("page not found", "this workspace is unavailable"),
    "Reddit": ("sorry, nobody on reddit goes by that name",),
    "Medium": ("page not found",),
    "Dev.to": ("404", "not found"),
    "Keybase": ("key not found", "not found"),
    "Kaggle": ("404", "not found"),
}

HEADERS = {"User-Agent": "True-Osint/1.0 (educational use)"}
GITHUB_API = "https://api.github.com"
REQUEST_TIMEOUT = 10
MAX_USERNAME_CANDIDATES = 5
CONFIDENCE_SCORE = {"high": 3, "medium": 2, "low": 1}


def _http_get(url, params=None, json_accept=False):
    headers = dict(HEADERS)
    if json_accept:
        headers["Accept"] = "application/vnd.github+json"
    try:
        return requests.get(
            url,
            params=params,
            headers=headers,
            timeout=REQUEST_TIMEOUT,
            allow_redirects=True,
        )
    except requests.RequestException:
        return None


def _append_diagnostic(diagnostics, message):
    if message not in diagnostics:
        diagnostics.append(message)


def _normalize_email(email):
    return email.strip().lower()


def _build_username_candidates(username):
    clean = re.sub(r"[^A-Za-z0-9._-]", "", username.strip())
    if not clean:
        return []

    candidates = [clean]
    compact = re.sub(r"[._-]+", "", clean)
    if compact and compact not in candidates:
        candidates.append(compact)

    parts = [part for part in re.split(r"[._-]+", clean) if part]
    if len(parts) >= 2:
        first, last = parts[0], parts[-1]
        for candidate in (f"{first}{last}", f"{first}_{last}", f"{first}.{last}"):
            if candidate not in candidates:
                candidates.append(candidate)

    return candidates[:MAX_USERNAME_CANDIDATES]


def _profile_mentions_email(profile_url, email):
    response = _http_get(profile_url)
    if response is None or response.status_code != 200:
        return False, None
    return _normalize_email(email) in response.text.lower(), response.url


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


def _extract_github_public_email_accounts(email, diagnostics):
    found = []
    response = _http_get(
        f"{GITHUB_API}/search/users",
        params={"q": f"\"{email}\" in:email", "per_page": 10},
        json_accept=True,
    )
    if response is None:
        _append_diagnostic(diagnostics, "GitHub API indisponible temporairement.")
        return found
    if response.status_code in {403, 429}:
        _append_diagnostic(diagnostics, "Limite GitHub API atteinte, recherche partielle.")
        return found
    if response.status_code != 200:
        return found

    try:
        items = response.json().get("items", [])
    except ValueError:
        return found

    target = _normalize_email(email)
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

        public_email = _normalize_email(user.get("email") or "")
        if public_email != target:
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


def _extract_github_commit_accounts(email, diagnostics):
    found = []
    response = _http_get(
        f"{GITHUB_API}/search/commits",
        params={"q": f"author-email:{email}", "per_page": 20},
        json_accept=True,
    )
    if response is None:
        _append_diagnostic(diagnostics, "Recherche commits GitHub indisponible.")
        return found
    if response.status_code in {403, 429}:
        _append_diagnostic(diagnostics, "Limite GitHub API atteinte, certains comptes peuvent manquer.")
        return found
    if response.status_code != 200:
        return found

    try:
        commits = response.json().get("items", [])
    except ValueError:
        return found

    target = _normalize_email(email)
    seen_logins = set()
    for item in commits:
        commit_author = item.get("commit", {}).get("author", {})
        commit_email = _normalize_email(commit_author.get("email") or "")
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


def _extract_email_mentions(email, username):
    found = []
    for site, url_template in EMAIL_SCAN_SITES.items():
        candidate_url = url_template.format(username)
        has_email, resolved_url = _profile_mentions_email(candidate_url, email)
        if not has_email:
            continue
        found.append(
            {
                "site": site,
                "url": resolved_url or candidate_url,
                "source": "Public profile contains email",
                "confidence": "medium",
            }
        )
    return found


def _extract_username_based_accounts(username_candidates):
    found = []

    for username in username_candidates:
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
            if "login" in resolved_url.lower() or "signup" in resolved_url.lower():
                continue

            # Skip generic redirects without visible relation to tested username.
            if username_lower not in resolved_url.lower() and username_lower not in page_content[:5000]:
                continue

            found.append(
                {
                    "site": site,
                    "url": resolved_url,
                    "source": f"Username match from email local-part ({username})",
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
        if CONFIDENCE_SCORE.get(account.get("confidence", "low"), 1) > CONFIDENCE_SCORE.get(
            existing.get("confidence", "low"), 1
        ):
            by_url[url] = account

    return sorted(
        by_url.values(),
        key=lambda item: CONFIDENCE_SCORE.get(item.get("confidence", "low"), 1),
        reverse=True,
    )


def find_social_accounts(email, include_probable=True, return_details=False):
    diagnostics = []
    discovered_accounts = []

    username = extract_username(email).strip()
    username_candidates = _build_username_candidates(username)
    if not username_candidates:
        result = {"accounts": [], "diagnostics": ["Partie locale de l'email invalide."]}
        return result if return_details else result["accounts"]

    discovered_accounts.extend(_extract_gravatar_accounts(email))
    discovered_accounts.extend(_extract_github_public_email_accounts(email, diagnostics))
    discovered_accounts.extend(_extract_github_commit_accounts(email, diagnostics))
    discovered_accounts.extend(_extract_email_mentions(email, username_candidates[0]))

    if include_probable:
        discovered_accounts.extend(_extract_username_based_accounts(username_candidates))

    result = {"accounts": _dedupe_accounts(discovered_accounts), "diagnostics": diagnostics}
    return result if return_details else result["accounts"]
