import requests
import urllib.parse
import time
from typing import Dict, List


def session(token: str):
    s = requests.Session()
    s.headers.update({'Authorization': f'token {token}'})
    return s


def search(session: requests.Session, query: str):
    page = 1
    paths: Dict[str, List[str]] = {}
    while True:
        qs = urllib.parse.urlencode({
            'q': query,
            'per_page': 100,
            'page': page,
        })
        url = f'https://api.github.com/search/code?{qs}'
        response = session.get(url)
        if response.status_code == 403:
            # throttled.
            time.sleep(60.)
            continue
        page += 1
        r = response.json()
        # https://developer.github.com/v3/search/#search-code
        for item in r.get('items', []):
            paths.setdefault(item['path'], []).append(item['html_url'])
        if 'rel="next"' not in response.headers.get('Link', ''):
            break
        if int(response.headers.get('X-RateLimit-Remaining', '0')) < 5:
            # about to hit rate limit.
            time.sleep(60.)
            continue
    return paths


def get_project(path: str):
    # path = https://github.com/username/<PROJECT>/...
    return path.split('/')[4]
