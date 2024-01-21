import tomli
from typing import TypedDict, List
from .paginate import Paginador  # noqa


class Info(TypedDict):
    version: str
    description: str
    name: str
    authors: List[str]


def get_project_info() -> Info:

    info: Info = {
        "version": '',
        "description": '',
        "name": '',
        'authors': ['']
    }

    with open("pyproject.toml", "rb") as toml_file:
        toml_data = tomli.load(toml_file)
        info['version'] = toml_data["tool"]["poetry"]["version"]
        info['description'] = toml_data["tool"]["poetry"]["description"]
        info['name'] = toml_data["tool"]["poetry"]["name"]
        info['authors'] = toml_data["tool"]["poetry"]["authors"]

    return info


class ConsoleColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'  # fim da cor
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    @classmethod
    def header(cls, string: str) -> str:
        return cls.HEADER + string + cls.ENDC

    @classmethod
    def okblue(cls, string: str) -> str:
        return cls.OKBLUE + string + cls.ENDC

    @classmethod
    def okgreen(cls, string: str) -> str:
        return cls.OKGREEN + string + cls.ENDC

    @classmethod
    def warning(cls, string: str) -> str:
        return cls.WARNING + string + cls.ENDC

    @classmethod
    def fail(cls, string: str) -> str:
        return cls.FAIL + string + cls.ENDC

    @classmethod
    def bold(cls, string: str) -> str:
        return cls.BOLD + string + cls.ENDC

    @classmethod
    def underline(cls, string: str) -> str:
        return cls.UNDERLINE + string + cls.ENDC