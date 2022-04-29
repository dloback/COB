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
    return "COB/api/v1"

@app.route('/competicao', methods = ['GET', 'POST', 'PUT'])
def competicao():
    with get_mysql_conn() as conn:
        if(request.method == 'GET'):
            cursor  = conn.cursor(dictionary=True)
            cursor.execute(""" SELECT Id_Competicao, 
                                      Nome_Competicao, 
                                      Data_Inscricao, 
                                      Data_Fim, 
                                      Metrica_Competicao, 
                                      Tentativas_Competicao 
                                 FROM Competicao """)

            results = cursor.fetchall()
            return(jsonify(results))

        if(request.method == 'POST'):
            Nome_Competicao         = str(request.json['Nome_Competicao'])
            Data_Inscricao          = str(request.json['Data_Inscricao'])
            Metrica_Competicao      = str(request.json['Metrica_Competicao'])
            Tentativas_Competicao   = str(request.json['Tentativas_Competicao'])
            cursor                  = conn.cursor(dictionary=True)

            cursor.execute(""" SELECT Id_Competicao 
                                 FROM Competicao 
                                WHERE Nome_Competicao = '{0}'""".format(Nome_Competicao))
            valid = cursor.fetchone()

            if not bool(valid):
                cursor.execute("""  INSERT 
                                    INTO Competicao (Nome_Competicao, Data_Inscricao, Metrica_Competicao, Tentativas_Competicao) 
                                   VALUES ('{0}','{1}','{2}','{3}')""".format(Nome_Competicao, Data_Inscricao, Metrica_Competicao, Tentativas_Competicao))
                conn.commit()
                cursor.execute(" SELECT LAST_INSERT_ID() as Id_Competicao ")
                results = cursor.fetchone()
                return(jsonify(results))
            else:
                return {"code": "906", "name": "Err", "description":"Competição já existe no banco de dados"}

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
            else:
                return {"code": "901", "name": "Err", "description": "Competição não encontrada no banco de dados"}

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
            Resultado_Atleta    = str(request.json['Resultado_Atleta'])
            cursor              = conn.cursor(dictionary=True)
            cursor.execute(""" SELECT Id_Competicao, 
                                      Data_Inscricao, 
                                      Tentativas_Competicao 
                                 FROM Competicao 
                                WHERE Nome_Competicao = '{0}'""".format(Nome_Competicao))
            valid_Competicao = cursor.fetchone()

            if bool(valid_Competicao):
                cursor.execute(""" SELECT Id_Competicao 
                                     FROM Competicao 
                                    WHERE Data_Inscricao >= NOW() 
                                      AND Id_Competicao = '{0}'""".format(valid_Competicao['Id_Competicao']))
                valid_Data      = cursor.fetchone()
                Data_Inscricao  = int(dt.fromisoformat(str(valid_Competicao['Data_Inscricao'])).strftime('%Y%m%d'))
                Data_Final      = int(dt.fromisoformat(str(dt.today())).strftime('%Y%m%d'))

                if Data_Inscricao >= Data_Final:
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
                        cursor.execute(""" INSERT 
                                             INTO Atleta (Id_Competicao, Nome_Atleta, Resultado_Atleta) 
                                           VALUES ('{0}','{1}','{2}')""".format(valid_Competicao['Id_Competicao'], Nome_Atleta, Resultado_Atleta))
                        conn.commit()
                        cursor.execute(" SELECT LAST_INSERT_ID() AS Id_Atleta ")
                        results = cursor.fetchone()
                        return(jsonify(results))

                    else: return {"code": "904", "name": "Err", "description": "Quantidade de tentativas da Competição já preenchidas para o Atleta."}
                else: return {"code": "903", "name": "Err", "description": "Data de Registro fora do prazo para a competição."}
            else: return {"code": "902", "name": "Err", "description": "Competição não existe no banco de dados."}

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
                else: return {"code": "907", "name": "Err", "description": "Métrica da competição não existe para ranking."}
            else: return {"code": "905", "name": "Err", "description": "Competição não existe no banco de dados."}

@app.route('/api/v1', methods=["GET"])
def info_view():
    output = {
        'info': 'GET /api/v1',
        'competicao': 'GET /competicao',
        'competicao inserir': 'POST /competicao',
        'competicao fim': 'PUT /competicao',
        'atleta': 'GET /atleta',
        'atleta': 'POST /atleta',
        'ranking': 'GET /atleta/<Nome_Competicao>'
    }
    return jsonify(output)

@app.errorhandler(HTTPException)
def exception_handler(error):
    return(jsonify({"code": error.code, "name": error.name, "description": error.description}))

if __name__ == '__main__':
    app.run()