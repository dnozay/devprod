from click.testing import CliRunner
from unittest.mock import patch

from devprod import cli


def test_cli_main():
    result = CliRunner().invoke(cli.main, [])
    assert result.exit_code == 0


def test_cli_version():
    result = CliRunner().invoke(cli.main, ['version'])
    assert result.exit_code == 0


def test_cli_github():
    result = CliRunner().invoke(cli.main, ['github'])
    assert result.exit_code == 0


@patch('devprod.github.search')
def test_cli_github_search(search):
    result = CliRunner().invoke(cli.main, ['github', 'search'])
    assert result.exit_code == 2

    search.return_value = {'filepath': ['url1', 'url2']}
    result = CliRunner().invoke(cli.main, ['github', 'search', 'some-query'])
    assert result.exit_code == 0
    assert 'filepath' in result.stdout
    assert 'url1' in result.stdout
    assert 'url2' in result.stdout
