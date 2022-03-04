# Notas sobre como usar o gov.br em um aplicação Angular com backend.

O gov.br segue um protocolo chamado OpenID Connect. Biblioteca do angular pode ser a 
https://github.com/manfredsteyer/angular-oauth2-oidc

O endereço de autoconfiguração OIDC (também chamado de discovery) do gov.br de staging é
https://sso.staging.acesso.gov.br/.well-known/openid-configuration . Produção é 
https://sso.acesso.gov.br/.well-known/openid-configuration

Se não fosse pela necessidade de checar o nível da conta do usuário (ouro, prata, etc), 
por conta da confiabilidade do cadastro, poderia só usar essa lib aí e pronto.

Minha sugestão de um fluxo de login usando angular com backend (ou seja, padrão de projeto
backend for frontend).

* Login pelo frontend usando a biblioteca do angular. Obtém token de acesso do gov.br.
* Frontend submete o token a um endpoint de login da tua aplicação. [^0]
* Backend valida o token [^1]. O Gov.br não tem um endpoint de introspeção do token.
* Tua aplicação chama o endpoint de verificação das confiabilidades (https://manual-roteiro-integracao-login-unico.servicos.gov.br/pt/stable/iniciarintegracao.html#resultado-esperado-do-acesso-ao-servico-de-confiabilidade-cadastral-categorias) pra checar se o usuário têm o nível adequado e pegar foto, por exemplo.
* Se tudo isso deu certo, tu passa o id de usuário pra tua infra de autenticação já existente, pra fazer autorização
* Estando tudo certo, aí tu emite um “token de sessão” normalmente como tu já faz.

# FAQ

## Porque não simplesmente usar o token do gov.br como token da minha aplicação?

Se você não precisar controlar o tempo de sessão do usuário e tiver ok de usar 
 o tempo de sessão do token gov.br, tudo bem. Mas você ainda vai precisar checar as confiabilidades,
 porque é trivial criar um cadastro em nome de outra pessoa usando o nível mais básico (carrossel de perguntas),
 uma vez que os dados são vendidos livremente na internet. Não dá pra checar as confiabilidades só
 no javascript, porque é trivial de burlar isso no javascript. Eu não sei porque o token não vem com essa
 informação (existe um scopo chamado govbr_confiabilidades, mas ele deve estar desativado porque não vem nada
 lá).
 



[^0]: Se ela já tinha um endpoint pra usuário+senha, vai ser basicamente a mesma coisa. Só que em vez de receber usuário e senha, recebe um token.
[^1]: Provavelmente melhor usar uma lib pra isso, por conta da validação da chave criptográfica, validação do campo aud (audiência) do token, etc. No caso do gov.br provavelmente a validação do token automática vai falhar porque o protocolo determina que na url que contém as chaves (jwks_uri na url de autoconfiguração) haja pelo menos uma chave com uso setado como “SIG”, e isso não tem no gov.br (acho que é um bug). Então tu talvez tenha que manualmente pegar o JSON Web Key Set (na url apontada em jwks_uri)(https://auth0.com/docs/secure/tokens/json-web-tokens/json-web-key-set-properties) e pegar a primeira chave que tiver lá pra passar pra lib que decodifica o JWT. Exemplo de como fazer isso em Python está em https://github.com/weltonrodrigo/govbr_test/blob/3d82f2ccfe178eb0d0fc636beb7fa583a66251ab/token_request.py#L44
