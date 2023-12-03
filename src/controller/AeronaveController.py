import pandas as pd
from model.aeronaves import Aeronave
from conexion.mongo_queries import MongoQueries

class AeronaveController:
    def __init__(self):
        self.mongo = MongoQueries()
        
    def adicionar_aeronave(self) -> Aeronave:

        self.mongo.connect()

        codigoCalda = input("Código calda: ")
            
        nomeAeronave = input("Nome: ")

        self.mongo.db["TBL_AERONAVES"].insert_one({'cd_calda': codigoCalda, 'nm_aeronave': nomeAeronave})
        
        df_aeronave = self.recuperar_aeronave(codigoCalda)
        
        nova_aeronave = Aeronave(df_aeronave.cd_calda.values[0], df_aeronave.nm_aeronave.values[0])
        
        print(nova_aeronave.to_string())
        
        self.mongo.close()

        return nova_aeronave

    def atualizar_aeronave(self) -> Aeronave:
        self.mongo.connect()

        codigoCalda = (input("O código calda da aeronave que você deseja alterar: "))

        if not self.verifica_existencia_aeronave(codigoCalda):
            
            novo_nome = input("Nome (Novo): ")

            self.mongo.db["TBL_AERONAVES"].update_one({"cd_calda": f"{codigoCalda}"}, {"$set": {"nm_aeronave": f"{novo_nome}"}})
           
            df_aeronave = self.recuperar_aeronave(codigoCalda)
            
            aeronave_atualizado = Aeronave(df_aeronave.cd_calda.values[0], df_aeronave.nm_aeronave.values[0])
           
            print(aeronave_atualizado.to_string())
            
            self.mongo.close()

            return aeronave_atualizado
        else:
            print(f"O Código calda {codigoCalda} não existe.")
            return None

    def excluir_aeronave(self):
        self.mongo.connect()

        codigoCalda = input("Drecuperar_aeronaveigite o código calda da aeronave que deseja excluir: ")   

        
        if not self.verifica_existencia_aeronave(codigoCalda):            
            
            df_aeronave = self.recuperar_aeronave(codigoCalda)
            
            self.mongo.db["TBL_AERONAVES"].delete_one({'cd_calda': codigoCalda})            
            
            aeronave_excluido = Aeronave(df_aeronave.cd_calda.values[0], df_aeronave.nm_aeronave.values[0])
            self.mongo.close()
            print("Aeronave Removida com Sucesso!")
            print(aeronave_excluido.to_string())
        else:
            print(f"O código calda {codigoCalda} não existe.")

    def verifica_existencia_aeronave(self, codigoCalda:str=None, external: bool=False) -> bool:
        
        if external:
            self.mongo.connect()

        df_aeronave = pd.DataFrame(list(self.mongo.db["TBL_AERONAVES"].find({"cd_calda": f"{codigoCalda}"}, {"cd_calda": 1, "nm_aeronave": 1, "_id": 0})))
        
        if external:
            self.mongo.close()
        
        return df_aeronave.empty
    
    def recuperar_aeronave(self, cd_calda:str=None, external: bool=False) -> pd.DataFrame:
        
        if external:
            self.mongo.connect()

        df_aeronave = pd.DataFrame(list(self.mongo.db["TBL_AERONAVES"].find({"cd_calda": f"{cd_calda}"}, {"cd_calda": 1, "nm_aeronave": 1, "_id": 0})))

        if external:
            self.mongo.close()
         
        return df_aeronave
