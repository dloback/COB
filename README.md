# COB
Jogos Olímpicos - Com a chegada dos jogos olímpicos, fomos designados para construir uma API REST em Ruby/Python para o COB (Comitê Olímico Brasileiro), que será responsável por marcar e dizer os vencedores das seguintes modalidades:

100m rasos: Menor tempo vence
Lançamento de Dardo: Maior distância vence

Através da API, deveremos ser capazes de:

1 - Criar uma competição
2 - Cadastrar resultados para uma competição (todos os campos são obrigatórios)
3 - Finalizar uma competição
4 - Retornar o ranking da competição, exibindo a posição final de cada atleta

Detalhes:

A API não deve aceitar cadastros de resultados se a competição já estiver encerrada.

------------------------------------------------
# BANCO DE DADOS
MySQL

Executar script COB.sql para criação da estrutura de dados necessária para o projeto.

Editar arquivo DB_Conn.py e editar as configurações da string de conexão com o banco de dados.

------------------------------------------------
# LINGUAGEM E BIBLIOTECAS
A linguagem escolhida para o desenvolvimento da API foi Python, utilizando as bibliotecas:

Flask
pip install flask

Flask Restful
pip install flask_restful

Json
pip install json

Werkzeug
pip install Werkzeug

Datetime
pip install datetime

MySQL
pip install mysql-connector-python

------------------------------------------------
# MÉTODOS DA API

# HOME
Exibe todos os métodos da API

Requisição - GET
Endereço de acesso a API, sem parametros

Resposta - Status 200 OK
{
    'competicao': 'GET /competicao',
    'competicao inserir': 'POST /competicao',
    'competicao fim': 'PUT /competicao',
    'atleta': 'GET /atleta',
    'atleta': 'POST /atleta',
    'ranking': 'GET /atleta/<Nome_Competicao>'
}

------------------------------------------------
# COMPETIÇÃO

Requisição - GET - /competicao
Lista todas as competições cadastradas

Resposta - Status 200 OK
[
    {
        "Data_Fim": null,
        "Id_Competicao": 1,
        "Metrica_Competicao": "m",
        "Nome_Competicao": "100m classificatoria 1",
        "Tentativas_Competicao": 1
    },
    {
        "Data_Fim": "Sat, 30 Apr 2022 00:00:00 GMT",
        "Id_Competicao": 2,
        "Metrica_Competicao": "m",
        "Nome_Competicao": "100m classificatoria 2",
        "Tentativas_Competicao": 1
    }
]

------------------------------------------------

Requisição - POST - /competicao
Cadastra nova competições
Nome_Competicao - Nome de uma competição que deseja cadastrar
Metrica_Competicao - m (metros) ou s (segundos)
Tentativas_Competicao - Quantas tentativas na competição poderá ser cadastradas por atleta. Ex.: No caso da competição do lançamento de dardos, cada atleta terá 3 chances, e o resultado da competição deverá levar em conta o lançamento mais distante de cada atleta.

{
  "Nome_Competicao": "100m classificatoria 1", 
  "Metrica_Competicao": "s", 
  "Tentativas_Competicao": "1"
}

Resposta - Status 200 OK
Id_Competicao - Identificador único gerado pelo sistema

{
    "Id_Competicao": 1
}

Exceção
{"code": "908", "name": "Err", "description":"Métrica da Competição só pode ser s (segundos) ou m (metros)."}
{"code": "906", "name": "Err", "description":"Competição já existe no banco de dados."}

------------------------------------------------

Requisição - PUT - /competicao
Insere data fim de uma competições
Nome_Competicao - Nome de uma competição que deseja editar a data final
Data_Fim - Registro do fim da competição, formato AAAA-MM-DD. A API não deve aceitar cadastros de resultados se a competição já estiver encerrada.

{
  "Nome_Competicao": "100m classificatoria 2", 
  "Data_Fim": "2022-04-30"
}

Resposta - Status 200 OK
Id_Competicao - Retorna o identificador da competição como sucesso do registro

{
    "Id_Competicao": 2
}

Exceção
{"code": "901", "name": "Err", "description": "Competição não encontrada no banco de dados."}

------------------------------------------------
# ATLETA

Requisição - GET - /atleta
Lista todas os atletas cadastradas

Resposta - Status 200 OK

[
    {
        "Id_Atleta": 1,
        "Id_Competicao": 1,
        "Nome_Atleta": "João",
        "Resultado_Atleta": 11.834
    },
    {
        "Id_Atleta": 2,
        "Id_Competicao": 1,
        "Nome_Atleta": "PEdro",
        "Resultado_Atleta": 11.334
    },
    {
        "Id_Atleta": 3,
        "Id_Competicao": 1,
        "Nome_Atleta": "Marcelo",
        "Resultado_Atleta": 10.934
    },
    {
        "Id_Atleta": 4,
        "Id_Competicao": 1,
        "Nome_Atleta": "Gael",
        "Resultado_Atleta": 10.034
    }
]

------------------------------------------------

Requisição - POST - /atleta
Cadastra atleta e resultado para uma competição
Nome_Competicao - Nome de uma competição que deseja cadastrar o atleta
Nome_Atleta - Nome do atleta que deseja cadastrar para a competição
Resultado_Atleta - Tempo feito pelo atleta (Metrica_Competicao s (segundos)) ou distância do lançamento (Metrica_Competicao m (metros))

{
  "Nome_Competicao": "100m classificatoria 1", 
  "Nome_Atleta": "João",
  "Resultado_Atleta": "11.834"
}

Resposta - Status 200 OK
Id_Atleta - Identificador único gerado pelo sistema

{
    "Id_Atleta": 1
}

Exceção

{"code": "904", "name": "Err", "description": "Quantidade de tentativas da Competição já preenchidas para o Atleta."}
{"code": "903", "name": "Err", "description": "Data de Registro fora do prazo para a competição."}
{"code": "902", "name": "Err", "description": "Competição não existe no banco de dados."}

------------------------------------------------
# RANKING

Requisição - GET - /atleta/<Nome_Competicao>
Lista todas os atletas e resultados para uma determinada competição, informando suas posições. 

Resposta - Status 200 OK

[
    {
        "Data_Fim": null,
        "Id_Atleta": 4,
        "Melhor_Marca": 10.034,
        "Metrica_Competicao": "s",
        "Nome_Atleta": "Gael",
        "Nome_Competicao": "100m classificatoria 1",
        "Posicao": 1
    },
    {
        "Data_Fim": null,
        "Id_Atleta": 3,
        "Melhor_Marca": 10.934,
        "Metrica_Competicao": "s",
        "Nome_Atleta": "Marcelo",
        "Nome_Competicao": "100m classificatoria 1",
        "Posicao": 2
    },
    {
        "Data_Fim": null,
        "Id_Atleta": 2,
        "Melhor_Marca": 11.334,
        "Metrica_Competicao": "s",
        "Nome_Atleta": "PEdro",
        "Nome_Competicao": "100m classificatoria 1",
        "Posicao": 3
    },
    {
        "Data_Fim": null,
        "Id_Atleta": 1,
        "Melhor_Marca": 11.834,
        "Metrica_Competicao": "s",
        "Nome_Atleta": "João",
        "Nome_Competicao": "100m classificatoria 1",
        "Posicao": 4
    }
]

Exceção

{"code": "907", "name": "Err", "description": "Métrica da competição não existe para ranking."}
{"code": "905", "name": "Err", "description": "Competição não existe no banco de dados."}
{"code": "905", "name": "Err", "description": "Competição não existe no banco de dados."}
