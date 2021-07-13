# Teste da autenticação do gov.br

**É necessário que o órgão realize o cadastro no gov.br 
antes, através do envio do formulário de cadastro.**

Veja em https://manual-roteiro-integracao-login-unico.servicos.gov.br/pt/stable/

**ESTE REPOSITÓRIO NÃO É VINCULADO DE FORMA NENHUMA AO GOVERNO FEDERAL
E AS INFORMAÇÕES DISPONÍVEIS AQUI FORAM RETIRADAS DO MANUAL DE INTEGRAÇÃO. 
USE POR SUA CONTA E RISCO.**

## Como utilizar

Preencha o `config.yaml` com os dados cadastrados junto ao gov.br.
Os dados já preenchidos nesse arquivo correspondem ao ambiente staging do gov.br.

Rode o script dentro do virtualenv usando pipenv:

```shell
python -m pip install pipenv
pipenv shell
python main.py
```

Será aberto o browser na página de login, o usuário e senha serão
preenchidas automaticamente pelo browser e depois que você resolver o
captcha, será impresso no console o `acess_token` e o `id_token` do usuário.


## Help wanted

Seria interessante imprimir todas as informações disponíveis na API do gov.br,
como foto e dados da receita.

Seria interessante tb uma aplicação web completa, que possa ser usada para testar
totalmente a integração, exemplificando uma implementação da autenticação.

