import requests

DEVS = {
    "GitLab": "https://gitlab.com/{}",
    "Bitbucket": "https://bitbucket.org/{}",
}

DEFAULT_TIMEOUT = 5


def find_dev_accounts(username: str) -> dict:
    if not username:
        return {}

    username = username.strip()
    results = {}
    for platform, url_template in DEVS.items():
        url = url_template.format(username)
        try:
            r = requests.get(url, timeout=DEFAULT_TIMEOUT)
            if r.status_code == 200:
                results[platform] = url
        except requests.RequestException:
            continue
    return results
