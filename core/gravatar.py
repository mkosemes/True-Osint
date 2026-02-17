import hashlib
from typing import Optional

import requests


def gravatar_lookup(email: str, timeout: int = 5) -> Optional[str]:
    h = hashlib.md5(email.strip().lower().encode("utf-8")).hexdigest()
    url = f"https://www.gravatar.com/avatar/{h}?d=404"
    try:
        r = requests.get(url, timeout=timeout)
    except requests.RequestException:
        return None
    return url if r.status_code == 200 else None
