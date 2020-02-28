import os
import unittest
from unittest.mock import patch
import responses  # type: ignore

from devprod import github


FIXTURE_DIR = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'data',
)


def read_fixture(path: str):
    with open(os.path.join(FIXTURE_DIR, path), 'r') as f:
        return f.read()
    return ''


class TestGithub(unittest.TestCase):
    @patch('time.sleep')
    @responses.activate
    def test_search(self, sleep):
        base_url = 'https://api.github.com/search/code?q=%22from+devprod.env+import+load_environment%22&per_page=100'
        responses.add(
            responses.GET,
            f'{base_url}&page=1',
            body='please retry, request throttled',
            content_type='plain/text',
            status=403)
        responses.add(
            responses.GET,
            f'{base_url}&page=1',
            body=read_fixture('github_code_search.data'),
            content_type='application/json; charset=utf-8',
            headers={
                'Link': f'{base_url}&page=2; rel="next"',
                'X-RateLimit-Remaining': '1',
            },
            status=200)
        responses.add(
            responses.GET,
            f'{base_url}&page=2',
            body='{}',
            content_type='application/json; charset=utf-8',
            status=200)

        s = github.session('GITHUB_TOKEN')
        results = github.search(s, '"from devprod.env import load_environment"')

        assert results == {
            'tests/test_env.py': [
                'https://github.com/dnozay/devprod/blob/131ea4338eb41bab40000f1c97ca3480027de864/tests/test_env.py'
            ]
        }
        assert sleep.call_count == 2

    def test_get_project(self):
        url = 'https://github.com/dnozay/devprod/blob/131ea4338eb41bab40000f1c97ca3480027de864/tests/test_env.py'
        assert github.get_project(url) == 'devprod'
