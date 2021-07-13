import logging
from dataclasses import dataclass
from pathlib import Path
from typing import List

from yaml import load, Loader

fmt_str = '[%(asctime)s] %(levelname)s @ %(filename)s:%(lineno)d %(message)s'
logging.basicConfig(level=logging.INFO)

LL = logging.getLogger(__name__)


@dataclass
class User:
    cpf: str
    senha: str


@dataclass
class Config:
    redirect_uri: str
    authz_endpoint: str
    token_endpoint: str
    jwk_endpoint: str
    scopes: List[str]
    client_id: str
    client_secret: str
    response_type: str
    user: User

    def get_scopes_as_str(self):
        return " ".join(self.scopes)


def parse_config(filename):
    with open(filename) as f:
        config_obj = load(f, Loader=Loader)
        return Config(
            redirect_uri=get_key(config_obj, 'redirect_uri'),
            authz_endpoint=get_key(config_obj, 'authz_endpoint'),
            token_endpoint=get_key(config_obj, 'token_endpoint'),
            jwk_endpoint=get_key(config_obj, 'jwk_endpoint'),
            scopes=get_key(config_obj, 'scopes'),
            client_id=get_key(config_obj, 'client_id'),
            client_secret=get_key(config_obj, 'client_secret'),
            response_type=get_key(config_obj, 'response_type'),
            user=get_user(config_obj, 'user'),
        )


def get_user(config_obj, key):
    user_dict = get_key(config_obj, key)
    try:
        cpf, senha = user_dict['cpf'], user_dict['senha']
        return User(cpf, senha)
    except KeyError as err:
        LL.error(f'Error getting user credentials: {err}')


def get_key(config_obj, key):
    try:
        value = config_obj[key]
        return value
    except KeyError:
        LL.error(f'Missing config key {key}')


config=parse_config(Path(__file__).parent / 'config.yaml')
