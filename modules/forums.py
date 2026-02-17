import requests

FORUMS = {
    "Reddit": "https://www.reddit.com/user/{}",
    "Medium": "https://medium.com/@{}",
}

DEFAULT_TIMEOUT = 5


def find_forum_accounts(username: str) -> dict:
    if not username:
        return {}

    username = username.strip()
    found = {}
    for name, url_template in FORUMS.items():
        url = url_template.format(username)
        try:
            r = requests.get(url, timeout=DEFAULT_TIMEOUT)
            if r.status_code == 200:
                found[name] = url
        except requests.RequestException:
            continue
    return found
