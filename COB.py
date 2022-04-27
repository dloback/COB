from DB_Conn import get_mysql_conn

from flask import Flask, request, jsonify, abort
from flask_restful import Resource, Api
from json import dumps

app = Flask(__name__)
api = Api(app)

@app.route("/")
def Landpage():
    return "Bem Vindo!!!!!!"

@app.route("/Competicao")
def get():
    with get_mysql_conn() as conn:
        query = conn.execute("select * from Competicao")
        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
        return jsonify(result)

#def post(self):
#    Nome_Competicao = '100 metros livre'
#    Data_Inscricao = '10/01/2010'
#    Metrica_Competicao = 'm'
#    with get_mysql_conn() as conn:
#        conn.execute("INSERT INTO Competicao (Nome_Competicao, Data_Inscricao, Metrica_Competicao) VALUES ({0},{1},{2})".format(Nome_Competicao, Data_Inscricao, Metrica_Competicao))
#        query = conn.execute('select * from Competicao order by Id_Competicao desc limit 1')
#        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
#        return jsonify(result)

@app.errorhandler(404) 
def invalid_route(e): 
    return jsonify({'errorCode' : 404, 'message' : 'Route not found'})



if __name__ == '__main__':
    app.run()    

