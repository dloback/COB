from DB_Conn import get_mysql_conn
from flask import Flask, request, jsonify, abort
from flask_restful import Resource, Api
from json import dumps
from werkzeug.exceptions import HTTPException
from datetime import datetime as dt

app = Flask(__name__)
api = Api(app)

@app.route("/")
def home():
    output = {
        'competicao': 'GET /competicao',
        'competicao inserir': 'POST /competicao',
        'competicao fim': 'PUT /competicao',
        'atleta': 'GET /atleta',
        'atleta': 'POST /atleta',
        'ranking': 'GET /atleta/<Nome_Competicao>'
    }
    return jsonify(output)

@app.route('/competicao', methods = ['GET', 'POST', 'PUT'])
def competicao():
    with get_mysql_conn() as conn:
        if(request.method == 'GET'):
            cursor  = conn.cursor(dictionary=True)
            cursor.execute(""" SELECT Id_Competicao, 
                                      Nome_Competicao,
                                      Data_Fim, 
                                      Metrica_Competicao, 
                                      Tentativas_Competicao 
                                 FROM Competicao """)

            results = cursor.fetchall()
            return(jsonify(results))

        if(request.method == 'POST'):
            Nome_Competicao         = str(request.json['Nome_Competicao'])
            Metrica_Competicao      = str(request.json['Metrica_Competicao']).lower()
            Tentativas_Competicao   = str(request.json['Tentativas_Competicao'])
            cursor                  = conn.cursor(dictionary=True)

            cursor.execute(""" SELECT Id_Competicao 
                                 FROM Competicao 
                                WHERE Nome_Competicao = '{0}'""".format(Nome_Competicao))
            valid = cursor.fetchone()

            if not bool(valid):
                if Metrica_Competicao == 's' or Metrica_Competicao == 'm':
                    cursor.execute(""" INSERT INTO Competicao (Nome_Competicao, Metrica_Competicao, Tentativas_Competicao) 
                                    VALUES ('{0}','{1}','{2}')""".format(Nome_Competicao, Metrica_Competicao, Tentativas_Competicao))
                    conn.commit()
                    cursor.execute(" SELECT LAST_INSERT_ID() as Id_Competicao ")
                    results = cursor.fetchone()
                    return(jsonify(results))
                else: return {"code": "908", "name": "Err", "description":"M??trica da Competi????o s?? pode ser s (segundos) ou m (metros)."}
            else: return {"code": "906", "name": "Err", "description":"Competi????o j?? existe no banco de dados."}

        if(request.method == 'PUT'):
            Nome_Competicao     = str(request.json['Nome_Competicao'])
            Data_Fim            = str(request.json['Data_Fim'])
            cursor              = conn.cursor(dictionary=True)

            cursor.execute(""" SELECT Id_Competicao 
                                 FROM Competicao 
                                WHERE Nome_Competicao = '{0}'""".format(Nome_Competicao))
            valid = cursor.fetchone()

            if bool(valid):
                cursor.execute(""" UPDATE Competicao 
                                      SET Data_Fim ='{0}' 
                                    WHERE Id_Competicao = '{1}'""".format(Data_Fim, valid['Id_Competicao']))
                conn.commit()
                return(jsonify(valid))
            else: return {"code": "901", "name": "Err", "description": "Competi????o n??o encontrada no banco de dados."}

@app.route('/atleta', methods = ['GET', 'POST'])
def atleta():
    with get_mysql_conn() as conn:
        if(request.method == 'GET'):
            cursor  = conn.cursor(dictionary=True)
            cursor.execute(""" SELECT Id_Atleta,
                                      Nome_Atleta,
                                      Id_Competicao,
                                      Resultado_Atleta
                                 FROM Atleta""")
            results = cursor.fetchall()
            return(jsonify(results))

        if(request.method == 'POST'):
            Nome_Competicao     = str(request.json['Nome_Competicao'])
            Nome_Atleta         = str(request.json['Nome_Atleta'])
            Resultado_Atleta    = float(request.json['Resultado_Atleta'])
            cursor              = conn.cursor(dictionary=True)
            cursor.execute(""" SELECT Id_Competicao, 
                                      Data_Fim, 
                                      Tentativas_Competicao 
                                 FROM Competicao 
                                WHERE Nome_Competicao = '{0}'""".format(Nome_Competicao))
            valid_Competicao = cursor.fetchone()

            if bool(valid_Competicao):

                Data_Fim    = str("0" if valid_Competicao['Data_Fim'] is None else valid_Competicao['Data_Fim'])
                if Data_Fim != "0": 
                    Data_Fim = int(dt.fromisoformat(str(valid_Competicao['Data_Fim'])).strftime('%Y%m%d'))
                Data_Final  = int(dt.fromisoformat(str(dt.today())).strftime('%Y%m%d'))

                if Data_Fim == "0" or Data_Fim >= Data_Final:
                    cursor.execute(""" SELECT C.Tentativas_Competicao, count(A.id_Atleta) AS Tentativas_Atleta
                                         FROM Competicao C
                                        INNER JOIN Atleta A
                                           ON C.Id_Competicao = A.Id_Competicao
                                        WHERE A.Nome_Atleta = '{0}' 
                                          AND C.Id_Competicao = '{1}'""".format(Nome_Atleta, valid_Competicao['Id_Competicao']))
                    valid_Tentativas        = cursor.fetchone()
                    Tentativas_Atleta       = int(0 if valid_Tentativas['Tentativas_Atleta'] is None else valid_Tentativas['Tentativas_Atleta'])
                    Tentativas_Competicao   = int(1 if valid_Tentativas['Tentativas_Competicao'] is None else valid_Tentativas['Tentativas_Competicao'])
                    
                    if bool(valid_Tentativas) and (Tentativas_Atleta < Tentativas_Competicao):
                        cursor.execute(""" INSERT INTO Atleta (Id_Competicao, Nome_Atleta, Resultado_Atleta) 
                                           VALUES ('{0}','{1}','{2}')""".format(valid_Competicao['Id_Competicao'], Nome_Atleta, Resultado_Atleta))
                        conn.commit()
                        cursor.execute(" SELECT LAST_INSERT_ID() AS Id_Atleta ")
                        results = cursor.fetchone()
                        return(jsonify(results))

                    else: return {"code": "904", "name": "Err", "description": "Quantidade de tentativas da Competi????o j?? preenchidas para o Atleta."}
                else: return {"code": "903", "name": "Err", "description": "Data de Registro fora do prazo para a competi????o."}
            else: return {"code": "902", "name": "Err", "description": "Competi????o n??o existe no banco de dados."}

@app.route('/ranking/<Nome_Competicao>', methods = ['GET'])
def ranking(Nome_Competicao):
    with get_mysql_conn() as conn:
        if(request.method == 'GET'):
            cursor              = conn.cursor(dictionary=True)
            cursor.execute(""" SELECT Id_Competicao, 
                                      Data_Fim,
                                      Metrica_Competicao
                                 FROM Competicao 
                                WHERE Nome_Competicao = '{0}'""".format(Nome_Competicao))
            valid_Competicao = cursor.fetchone()
            if bool(valid_Competicao):
                if valid_Competicao['Metrica_Competicao'] == 'm':
                    cursor  = conn.cursor(dictionary=True)
                    cursor.execute(""" SELECT A.Id_Atleta, A.Nome_Atleta, MAX(A.Resultado_Atleta) AS Melhor_Marca, 
                                              B.Nome_Competicao, 
                                              B.Data_Fim, 
                                              B.Metrica_Competicao,
                                              ROW_NUMBER() OVER (ORDER BY MAX(A.Resultado_Atleta) DESC) Posicao
                                         FROM Atleta A
                                        INNER JOIN Competicao B
                                           ON A.Id_Competicao = B.Id_Competicao
                                        WHERE A.Id_Competicao = '{0}'
                                        GROUP BY A.Nome_Atleta
                                        ORDER BY Posicao""".format(valid_Competicao['Id_Competicao'])) 
                    results = cursor.fetchall()
                    return(jsonify(results))
                elif valid_Competicao['Metrica_Competicao'] == 's':
                    cursor  = conn.cursor(dictionary=True)
                    cursor.execute(""" SELECT A.Id_Atleta, A.Nome_Atleta, MIN(A.Resultado_Atleta) AS Melhor_Marca, 
                                              B.Nome_Competicao, 
                                              B.Data_Fim, 
                                              B.Metrica_Competicao,
                                              ROW_NUMBER() OVER (ORDER BY MIN(A.Resultado_Atleta)) Posicao
                                         FROM Atleta A
                                        INNER JOIN Competicao B
                                           ON A.Id_Competicao = B.Id_Competicao
                                        WHERE A.Id_Competicao = '{0}'
                                        GROUP BY A.Nome_Atleta
                                        ORDER BY Posicao""".format(valid_Competicao['Id_Competicao'])) 
                    results = cursor.fetchall()
                    return(jsonify(results))
                else: return {"code": "907", "name": "Err", "description": "M??trica da competi????o n??o existe para ranking."}
            else: return {"code": "905", "name": "Err", "description": "Competi????o n??o existe no banco de dados."}

@app.errorhandler(HTTPException)
def exception_handler(error):
    return(jsonify({"code": error.code, "name": error.name, "description": error.description}))

if __name__ == '__main__':
    app.run()