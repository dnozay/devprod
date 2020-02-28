import click

from .version import __version__


@click.group()
def main():
    pass


@main.group()
def github():
    pass


@github.command('search')
@click.argument('query')
def github_search(query):
    from devprod import env
    from devprod.github import session, search
    env.load_environment(['GITHUB_TOKEN'])
    s = session(env.GITHUB_TOKEN)
    results = search(s, query)
    for path in sorted(results.keys()):
        print(f'{path}:')
        for url in results[path]:
            print(f'\t- {url}')
        print('')


@main.command()
def version():
    print(f'version: {__version__}')
