import hashlib
import requests

REQUEST_TIMEOUT = 8


def gravatar_hash(email):
    return hashlib.md5(email.strip().lower().encode()).hexdigest()


def gravatar_lookup(email):
    h = gravatar_hash(email)
    url = f"https://www.gravatar.com/avatar/{h}?d=404"
    try:
        r = requests.get(url, timeout=REQUEST_TIMEOUT)
        return url if r.status_code == 200 else None
    except requests.RequestException:
        return None


def gravatar_profile_lookup(email):
    h = gravatar_hash(email)
    profile_url = f"https://www.gravatar.com/{h}.json"

    try:
        response = requests.get(profile_url, timeout=REQUEST_TIMEOUT)
        if response.status_code != 200:
            return None
        payload = response.json()
    except (requests.RequestException, ValueError):
        return None

    entries = payload.get("entry", [])
    if not entries:
        return None
    return entries[0]
