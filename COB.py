from DB_Conn import get_mysql_conn

from flask import Flask, request, jsonify, abort
from flask_restful import Resource, Api
from json import dumps
from werkzeug.exceptions import HTTPException

app = Flask(__name__)
api = Api(app)

@app.route("/")
def Landpage():
    return "Bem Vindo!!!!!!"

@app.route('/competicao', methods = ['GET', 'POST'])
def competicao():
    with get_mysql_conn() as conn:
        if(request.method == 'GET'):
            cursor  = conn.cursor(dictionary=True)
            cursor.execute("select * from Competicao")
            results = cursor.fetchall()
            return(jsonify(results))

        if(request.method == 'POST'):
            Nome_Competicao     = str(request.json['Nome_Competicao'])
            Data_Inscricao      = str(request.json['Data_Inscricao'])
            Metrica_Competicao  = str(request.json['Metrica_Competicao'])
            cursor  = conn.cursor(dictionary=True)

            cursor.execute("SELECT Id_Competicao From Competicao Where Nome_Competicao = '{0}'".format(Nome_Competicao))
            valid = cursor.fetchone()

            if not bool(valid):
                insert_competicao = """Insert Into Competicao (Nome_Competicao, Data_Inscricao, Metrica_Competicao) values ('{0}','{1}','{2}')""".format(Nome_Competicao, Data_Inscricao, Metrica_Competicao)
                print(insert_competicao)
                cursor.execute(insert_competicao)
                conn.commit()
                cursor.execute("SELECT LAST_INSERT_ID() as Id_Competicao")
                results = cursor.fetchone()
                return(jsonify(results))
            else:
                return {"Err": "Competição já existe no banco de dados"}

@app.route('/atleta', methods = ['GET', 'POST'])
def atleta():
    with get_mysql_conn() as conn:
        if(request.method == 'GET'):
            cursor  = conn.cursor(dictionary=True)
            cursor.execute("select * from Atleta")
            results = cursor.fetchall()
            return(jsonify(results))

@app.route('/api/v1', methods=["GET"])
def info_view():
    output = {
        'info': 'GET /api/v1',
        'competicao': 'GET /competicao',
        'inserir competicao': 'POST /competicao',
    }
    return jsonify(output)



@app.errorhandler(HTTPException)
def exception_handler(error):
    return(jsonify({"code": error.code, "name": error.name, "description": error.description,}))

if __name__ == '__main__':
    app.run()