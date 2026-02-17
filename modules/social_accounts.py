import requests

SOCIAL_SITES = {
    "GitHub": "https://github.com/{}",
    "Twitter": "https://twitter.com/{}",
    "Instagram": "https://www.instagram.com/{}",
    "Facebook": "https://www.facebook.com/{}",
    "Reddit": "https://www.reddit.com/user/{}",
    "Medium": "https://medium.com/@{}"
}

DEFAULT_TIMEOUT = 5


def find_social_accounts(username: str) -> dict:
    if not username:
        return {}

    username = username.strip()
    results = {}
    for site, url_template in SOCIAL_SITES.items():
        url = url_template.format(username)
        try:
            r = requests.get(url, timeout=DEFAULT_TIMEOUT)
            if r.status_code == 200:
                results[site] = url
        except requests.RequestException:
            continue
    return results
