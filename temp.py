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
def get(self):
    with get_mysql_conn() as conn:
        query = conn.execute("select * from Competicao")
        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
        return jsonify(result)

def post(self):
    Nome_Competicao = "100 metros livre"
    Data_Inscricao = '10/01/2010'
    Metrica_Competicao = 'm'
    with get_mysql_conn() as conn:
        conn.execute("INSERT INTO Competicao (Nome_Competicao, Data_Inscricao, Metrica_Competicao) VALUES ({0},{1},{2}')".format(Nome_Competicao, Data_Inscricao, Metrica_Competicao))
        query = conn.execute('select * from Competicao order by Id_Competicao desc limit 1')
        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
        return jsonify(result)

@app.errorhandler(404) 
def invalid_route(e): 
    return jsonify({'errorCode' : 404, 'message' : 'Route not found'})


'''    
with get_mysql_conn() as conn:

    consulta_sql = "select * from Competicao"

    cursor = conn.cursor()
    cursor.execute(consulta_sql)
    linhas = cursor.fetchall()
    print("Número total de registros retornados: ", cursor.rowcount)

class Competicao(Resource):
    def get(self):
        query = conn.execute("select * from Competicao")
        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
        return jsonify(result)

    def post(self):
        name = request.json['name']
        email = request.json['email']

        conn.execute(
            "insert into user values(null, '{0}','{1}')".format(name, email))

        query = conn.execute('select * from user order by id desc limit 1')
        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
        return jsonify(result)

    def put(self):
        id = request.json['id']
        name = request.json['name']
        email = request.json['email']

        conn.execute("update user set name ='" + str(name) +
                     "', email ='" + str(email) + "'  where id =%d " % int(id))

        query = conn.execute("select * from user where id=%d " % int(id))
        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
        return jsonify(result)

class UserById(Resource):
    def delete(self, id):
        conn.execute("delete from user where id=%d " % int(id))
        return {"status": "success"}

    def get(self, id):
        query = conn.execute("select * from user where id =%d " % int(id))
        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
        return jsonify(result)


api.add_resource(Competicao, '/users') 
#api.add_resource(UserById, '/users/<id>') 
'''

if __name__ == '__main__':
    app.run()    

