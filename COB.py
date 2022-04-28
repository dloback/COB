from DB_Conn import get_mysql_conn

from flask import Flask, request, jsonify, abort
from flask_restful import Resource, Api
from json import dumps
from werkzeug.exceptions import HTTPException
from datetime import datetime as dt

app = Flask(__name__)
api = Api(app)

@app.route("/")
def Landpage():
    return "Bem Vindo!!!!!!"

@app.route('/competicao', methods = ['GET', 'POST', 'PUT'])
def competicao():
    with get_mysql_conn() as conn:
        if(request.method == 'GET'):
            cursor  = conn.cursor(dictionary=True)
            cursor.execute("select * from Competicao")
            results = cursor.fetchall()
            return(jsonify(results))

        if(request.method == 'POST'):
            Nome_Competicao         = str(request.json['Nome_Competicao'])
            Data_Inscricao          = str(request.json['Data_Inscricao'])
            Metrica_Competicao      = str(request.json['Metrica_Competicao'])
            Tentativas_Competicao   = str(request.json['Tentativas_Competicao'])
            cursor                  = conn.cursor(dictionary=True)

            cursor.execute("SELECT Id_Competicao From Competicao Where Nome_Competicao = '{0}'".format(Nome_Competicao))
            valid = cursor.fetchone()

            if not bool(valid):
                cursor.execute("Insert Into Competicao (Nome_Competicao, Data_Inscricao, Metrica_Competicao, Tentativas_Competicao) values ('{0}','{1}','{2}','{3}')".format(Nome_Competicao, Data_Inscricao, Metrica_Competicao, Tentativas_Competicao))
                conn.commit()
                cursor.execute("SELECT LAST_INSERT_ID() as Id_Competicao")
                results = cursor.fetchone()
                return(jsonify(results))
            else:
                return {"Err": "Competição já existe no banco de dados"}

        if(request.method == 'PUT'):
            Nome_Competicao     = str(request.json['Nome_Competicao'])
            Data_Fim            = str(request.json['Data_Fim'])
            cursor              = conn.cursor(dictionary=True)

            cursor.execute("SELECT Id_Competicao From Competicao Where Nome_Competicao = '{0}'".format(Nome_Competicao))
            valid = cursor.fetchone()

            if bool(valid):
                cursor.execute("Update Competicao set Data_Fim ='{0}' Where Id_Competicao = '{1}'".format(Data_Fim, valid['Id_Competicao']))
                conn.commit()
                return(jsonify(valid))
            else:
                return {"Err": "Competição não encontrada no banco de dados"}

@app.route('/atleta', methods = ['GET', 'POST'])
def atleta():
    with get_mysql_conn() as conn:
        if(request.method == 'GET'):
            cursor  = conn.cursor(dictionary=True)
            cursor.execute("select * from Atleta")
            results = cursor.fetchall()
            return(jsonify(results))

        if(request.method == 'POST'):
            Nome_Competicao     = str(request.json['Nome_Competicao'])
            Nome_Atleta         = str(request.json['Nome_Atleta'])
            Resultado_Atleta    = str(request.json['Resultado_Atleta'])
            cursor              = conn.cursor(dictionary=True)
            cursor.execute("SELECT Id_Competicao, Data_Inscricao, Tentativas_Competicao From Competicao Where Nome_Competicao = '{0}'".format(Nome_Competicao))
            valid_Competicao = cursor.fetchone()

            if bool(valid_Competicao):
                cursor.execute("SELECT Id_Competicao From Competicao Where Data_Inscricao >= NOW() AND Id_Competicao = '{0}'".format(valid_Competicao['Id_Competicao']))
                valid_Data      = cursor.fetchone()
                Data_Inscricao  = int(dt.fromisoformat(str(valid_Competicao['Data_Inscricao'])).strftime('%Y%m%d'))
                Data_Final      = int(dt.fromisoformat(str(dt.today())).strftime('%Y%m%d'))

                if Data_Inscricao >= Data_Final:
                    cursor.execute("""  Select C.Tentativas_Competicao, count(A.id_Atleta) as Tentativas_Atleta
                                          From Competicao C
                                         Inner Join Atleta A
                                            On C.Id_Competicao = A.Id_Competicao
                                         Where A.Nome_Atleta = '{0}' 
                                           AND C.Id_Competicao = '{1}'""".format(Nome_Atleta, valid_Competicao['Id_Competicao']))
                    valid_Tentativas        = cursor.fetchone()
                    Tentativas_Atleta       = int(0 if valid_Tentativas['Tentativas_Atleta'] is None else valid_Tentativas['Tentativas_Atleta'])
                    Tentativas_Competicao   = int(1 if valid_Tentativas['Tentativas_Competicao'] is None else valid_Tentativas['Tentativas_Competicao'])
                    
                    if bool(valid_Tentativas) and (Tentativas_Atleta < Tentativas_Competicao):
                        cursor.execute("Insert Into Atleta (Id_Competicao, Nome_Atleta, Resultado_Atleta) values ('{0}','{1}','{2}')".format(valid_Competicao['Id_Competicao'], Nome_Atleta, Resultado_Atleta))
                        conn.commit()
                        cursor.execute("SELECT LAST_INSERT_ID() as Id_Atleta")
                        results = cursor.fetchone()
                        return(jsonify(results))
                        
                    else: return {"Err": "Quantidade de tentativas da Competição já preenchidas para o Atleta."}
                else: return {"Err": "Data de Registro fora do prazo para a competição."}
            else: return {"Err": "Competição não existe no banco de dados."}

@app.route('/api/v1', methods=["GET"])
def info_view():
    output = {
        'info': 'GET /api/v1',
        'competicao': 'GET /competicao',
        'competicao inserir': 'POST /competicao',
        'competicao fim': 'PUT /competicao',
        'atleta': 'GET /atleta',
    }
    return jsonify(output)

@app.errorhandler(HTTPException)
def exception_handler(error):
    return(jsonify({"code": error.code, "name": error.name, "description": error.description,}))

if __name__ == '__main__':
    app.run()