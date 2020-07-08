import click

from devprod.version import __version__
from devprod import env


@click.group()
def main():
    pass


@main.group()
def github():
    pass


@github.command('search')
@click.argument('query')
def github_search(query):
    from devprod.github import session, search
    env.load_environment(['GITHUB_TOKEN'])
    s = session(env.GITHUB_TOKEN)
    results = search(s, query)
    for path in sorted(results.keys()):
        print(f'{path}:')
        for url in results[path]:
            print(f'\t- {url}')
        print('')


@main.group()
def sem1():
    pass


@sem1.command('projects')
@click.argument('organization')
def sem1_projects(organization):
    from devprod.semaphore_classic import session, get_projects
    env.load_environment(['SEMAPHORE1_TOKEN'])
    s = session(env.SEMAPHORE1_TOKEN)
    projects = get_projects(s, organization)
    for project in projects:
        print(f'{project["id"]} {organization}/{project["name"]} => {project["html_url"]}')


@sem1.command('project:config')
@click.argument('organization')
@click.argument('project')
def sem1_project_config(organization, project):
    from devprod.semaphore_classic import session, get_project_config, get_project_secrets
    env.load_environment(['SEMAPHORE1_TOKEN'])
    s = session(env.SEMAPHORE1_TOKEN)
    secrets = get_project_secrets(s, env.SEMAPHORE1_TOKEN, organization, project)
    config = get_project_config(s, env.SEMAPHORE1_TOKEN, organization, project)
    for block in config:
        print(f'{block["type"]} name={block["name"]}')
        for command in block.get('commands', []):
            print(f'\t{command}')
        print('')


@main.command()
def version():
    print(f'version: {__version__}')
