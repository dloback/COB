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
    if(request.method == 'GET'):
        with get_mysql_conn() as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("select Id_Competicao, Nome_Competicao from Competicao")
            results = cursor.fetchall()
            return(jsonify(results))


@app.route('/atleta', methods = ['GET', 'POST'])
def atleta():
    if(request.method == 'GET'):
        with get_mysql_conn() as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("select * from Atleta")
            results = cursor.fetchall()
            return(jsonify(results))


@app.errorhandler(Exception)
def exception_handler(error):
    return(jsonify({"code": error.code, "name": error.name, "description": error.description,}))

if __name__ == '__main__':
    app.run()