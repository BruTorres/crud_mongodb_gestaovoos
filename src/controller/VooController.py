import pandas as pd   
from bson import ObjectId
from reports.relatorios import Relatorio
from model.voos import Voo
from model.aeronaves import Aeronave
from controller.AeronaveController import AeronaveController
from conexion.mongo_queries import MongoQueries
from datetime import datetime

class VooController:
    def __init__(self):
        self.ctrl_aeronave = AeronaveController()
        self.mongo = MongoQueries()
        self.relatorio = Relatorio()
        
    def inserir_voo(self) -> Voo:
        self.mongo.connect()
        
        dt_voo_str = input("Digite a data do voo (yyyy-mm-dd): ")

        cd_calda = input("Digite o código calda da aeronave que você deseja: ")
        aeronave = self.valida_aeronave(cd_calda)
        if aeronave is None:
            return None

        data = {
            "nr_voo": Voo.get_numeroVoo(),  # A função get_numeroVoo precisa ser corretamente chamada
            "dt_voo": dt_voo_str,
            "cd_calda": aeronave.get_codigoCalda()
        }

        id_voo = self.mongo.db["TBL_VOOS"].insert_one(data)

        df_voo = self.recuperar_voo(id_voo.inserted_id)
        
        novo_voo = Voo(df_voo.nr_voo.values[0], df_voo.dt_voo.values[0], df_voo.cd_calda[0])
        
        print(novo_voo.to_string())
        
        return novo_voo

    def atualizar_voo(self) -> Voo:
        self.mongo.connect()

        nr_voo = int(input("Digite o número do voo que será alterado: "))        

        if not self.verifica_existencia_voo(nr_voo):

            cd_calda = str(input("Digite o código calda da aeronave que você deseja: "))
            aeronave = self.valida_aeronave(cd_calda)
            if aeronave is None:
                return None

            dt_voo_str = input("Digite a data do voo (yyyy-mm-dd): ")
        
            data = {
                "cd_calda": aeronave.get_codigoCalda(),
                "dt_voo": dt_voo_str
            }
            
            self.mongo.db['TBL_VOOS'].update_one({"nr_voo": nr_voo}, {"$set": data})
            
            df_voo = pd.DataFrame(list(self.mongo.db['TBL_VOOS'].find({"nr_voo": nr_voo})))
            
            voo_atualizado = Voo(df_voo.nr_voo.values[0], df_voo.cd_calda.values[0], df_voo.dt_voo.values[0])
            
            print(voo_atualizado.to_string())
            
            return voo_atualizado
        else:
            print(f"O número do voo {nr_voo} não existe.")
            return None

    def excluir_voo(self):
        nr_voo = int(input("Digite o número do voo que será excluído: "))           

        self.mongo.db['TBL_VOOS'].delete_one({"nr_voo": nr_voo})

        print("Voo removido com sucesso!")

    def verifica_existencia_voo(self, nr_voo:int=None) -> bool:
        df_voo = pd.DataFrame(list(self.mongo.db["TBL_VOOS"].find({"nr_voo": nr_voo})))
        return df_voo.empty
    
    def valida_aeronave(self, cd_calda:str=None) -> Aeronave:
        if self.ctrl_aeronave.verifica_existencia_aeronave(cd_calda):
            print(f"O código calda {cd_calda} informado não existe.")
            return None
        else:
            df_aeronave = pd.DataFrame(list(self.mongo.db["TBL_AERONAVES"].find({"cd_calda": cd_calda})))
            aeronave = Aeronave(df_aeronave.cd_calda.values[0], df_aeronave.nm_aeronave.values[0])
            return aeronave
        
    def recuperar_voo(self, id_voo:int=None) -> pd.DataFrame:
        df_voo = pd.DataFrame(list(self.mongo.db["TBL_VOOS"].find({"_id": id_voo})))
        return df_voo
