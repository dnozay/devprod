import unittest
from unittest.mock import patch

from devprod.env import load_environment


class TestEnvModule(unittest.TestCase):
    @patch.dict('os.environ', {}, clear=True)
    def test_load_environment_negative(self):
        with self.assertRaises(RuntimeError):
            load_environment(['GITHUB_TOKEN'])

    @patch.dict('os.environ', {'GITHUB_TOKEN': 'test'}, clear=True)
    def test_load_environment_positive(self):
        load_environment(['GITHUB_TOKEN'])
