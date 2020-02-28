import os
from typing import List


def load_environment(variables: List[str]):
    for name in variables:
        value = os.environ.get(name)
        if value is None:
            raise RuntimeError(f'please export {name}')
        globals()[name] = value
