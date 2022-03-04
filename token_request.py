import json
from pathlib import Path
from pprint import pformat
from typing import Tuple

import jwt as jwt
import pendulum as pendulum
import requests
from jwt import PyJWKClient

from config import config, logging

JWK_CLIENT = PyJWKClient(config.jwk_endpoint)
SIGNING_KEY = JWK_CLIENT.get_jwk_set().keys[0]

LL = logging.getLogger(__name__)


def request_token(code):
    auth = (config.client_id, config.client_secret)
    params = {
        'client_id': config.client_id,
        'client_secret': config.client_secret,
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': config.redirect_uri,
    }
    res = requests.post(config.token_endpoint, data=params, auth=auth)
    try:
        obj = res.json()
        tokens = obj['access_token'], obj['id_token']
        access_token, id_token = pretty_print(tokens)
        LL.info(f'Resposta do Token Endpoint: {json.dumps(obj, indent=2)}')
        LL.info(f'Access Token: {access_token}')
        LL.info(f'ID Token: {id_token}')
    except:
        LL.error(f'Erro ao obter token: {res.json()}')


def pretty_print(tokens: Tuple[str, str]):
    return [decode_token(token) for token in tokens]


def decode_token(token: str):
    try:
        decoded = jwt.decode(
            jwt=token,
            audience=config.client_id,
            # Necessário indicar qual a chave a ser usada porque
            # o keyset do gov.br não aponta a chave com 'use':'sig'
            key=SIGNING_KEY.key,
            algorithms=['RS256']
        )
        decoded['exp'] = pendulum.from_timestamp(
            decoded['exp']).diff_for_humans()
        decoded['iat'] = pendulum.from_timestamp(
            decoded['iat']).diff_for_humans()
    except Exception as err:
        decoded = ""
        LL.error(err)

    return pformat(decoded)


if __name__ == '__main__':
    """Teste do código.
    Salve o json de retorno do endpoint token em test_resources/test_token.json
    """

    filename = Path(__file__).parent / "test_resources/test_token.json"
    token_set = json.load(filename.open())
    LL.info(pretty_print(token_set))
