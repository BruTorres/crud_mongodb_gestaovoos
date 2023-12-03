from conexion.mongo_queries import MongoQueries
import pandas as pd
from pymongo import ASCENDING, DESCENDING

class Relatorio:
    def __init__(self):
        pass

    def get_relatorio_aeronaves(self):
        # Cria uma nova conexão com o banco
        mongo = MongoQueries()
        mongo.connect()
        # Recupera os dados transformando em um DataFrame
        query_result = mongo.db["TBL_AERONAVES"].find({}, 
                                                 {"cd_calda": 1, 
                                                  "nm_aeronave": 1, 
                                                  "_id": 0
                                                 }).sort("nm_aeronave", ASCENDING)
        df_aeronave = pd.DataFrame(list(query_result))
        # Fecha a conexão com o mongo
        mongo.close()
        print(df_aeronave)
        input("Pressione Enter para Sair do Relatório de Aeronaves")


    def get_relatorio_voos(self):
        # Cria uma nova conexão com o banco
        mongo = MongoQueries()
        mongo.connect()
        # Realiza uma consulta no mongo e retorna o cursor resultante para a variável
        query_result = mongo.db['TBL_VOOS'].aggregate([
                                                    {
                                                        '$lookup': {
                                                            'from': 'TBL_AERONAVES', 
                                                            'localField': 'cd_calda', 
                                                            'foreignField': 'cd_calda', 
                                                            'as': 'AERONAVES'
                                                    }
                                                    }, {
                                                        '$unwind': {
                                                            'path': '$AERONAVES'
                                                        }
                                                    }, {
                                                        '$project': {
                                                            'nr_voo': 1, 
                                                            'dt_voo': 1, 
                                                            'cd_calda': 1, 
                                                            'aeronave': '$AERONAVES.nm_aeronave', 
                                                            '_id': 0
                                                        }
                                                    }, {
                                                        '$sort': {
                                                            'aeronave': 1
                                                        }
                                                    }
                                                    ])
        df_tbl_voos = pd.DataFrame(list(query_result))

        mongo.close()
        print(df_tbl_voos[["nr_voo", "dt_voo", "cd_calda", "aeronave"]])

        input("Pressione Enter para Sair do Relatório de Voos")

    def get_relatorio_total_aeronave(self):
        # Cria uma nova conexão com o banco
        mongo = MongoQueries()
        mongo.connect()
        # Recupera os dados transformando em um DataFrame
        query_result = mongo.db["TBL_AERONAVES"].aggregate([{
                                                "$project": {
                                                'cd_calda': 1,
                                                'nm_aeronave': 1,
                                                '_id': 0
                                            }
        }])
        df_aeronave = pd.DataFrame(list(query_result))
        # Fecha a conexão com o mongo
        mongo.close()
        relatorio = df_aeronave.groupby('nm_aeronave').size().reset_index(name='total_aeronaves')

        print(relatorio)
        input("Pressione Enter para Sair do Relatório de Aeronaves")