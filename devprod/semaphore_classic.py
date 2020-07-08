import requests
import time
from typing import Dict, List, Union

Session = requests.Session
OneObject = Dict[str, str]
ManyObjects = List[OneObject]


def session(token: str):
    s = Session()
    s.headers.update({'Authorization': f'Token {token}'})
    return s


def api_v2(session: Session, api_url: str) -> Union[OneObject, ManyObjects]:
    page = 1
    items: ManyObjects = []
    while True:
        url = f'https://api.semaphoreci.com/v2/{api_url}?page={page}'
        response = session.get(url)
        if response.status_code == 429:
            print('throttled')
            # throttled.
            time.sleep(60.)
            continue
        page += 1
        # https://semaphoreci.com/docs/api-v2-overview.html
        r = response.json()
        if isinstance(r, dict):
            return r
        items += r
        if len(r) < int(response.headers.get('Per-Page', '30')):
            break
        if 'rel="next"' not in response.headers.get('Link', ''):
            break
    return items


def get_projects(session: Session, organization: str):
    return api_v2(session, f'/orgs/{organization}/projects')


def get_project_config(session: Session, token: str, organization: str, project: str):
    config_url = f'https://semaphoreci.com/api/internal/{organization}/{project}/thread_configs'
    data = {'auth_token': token}  # does not support session auth
    response = requests.get(config_url, data)
    return response.json()


def get_project_secrets(session: Session, token: str, organization: str, project: str):
    project_url = f'https://api.semaphoreci.com/v2/orgs/{organization}/projects?name={project}'
    response = session.get(project_url)
    if response.status_code != 200:
        return {}

    project_info = response.json()[0]
    project_id = project_info['id']

    # secrets
    secrets_url = project_info['secrets_url']
    response = session.get(secrets_url)
    if response.status_code != 200:
        return {}

    # env_vars
    env_vars_url = f'https://api.semaphoreci.com/v2/projects/{project_id}/env_vars'
    response = session.get(env_vars_url)
    if response.status_code != 200:
        return {}

    env_vars = {}
    for env_var in response.json():
        pass

    return {}