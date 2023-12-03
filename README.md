# Exemplo de Sistema em Python fazendo CRUD no MongoDB

Esse sistema de exemplo é composto por um conjunto de coleções(collections) que representam pedidos de vendas, contendo coleções como: voos e aeronaves

O sistema exige que as coleções existam, então basta executar o script Python a seguir para criação das coleções e preenchimento de dados de exemplos:
```shell
~$ python createCollectionsAndData.py
```
**Atenção: tendo em vista que esse projeto é continuidade do [crud_oracle_gestaovoos-main3], é importante que as tabelas do Oracle existam e estejam preenchidas, pois o script _createCollectionsAndData.py_ irá realizar uma consulta em cada uma das tabelas e preencher as _collections_ com os novos _documents_.**

Para executar o sistema basta executar o script Python a seguir:
```shell
~$ python principal.py
```

## Organização
- [diagrams](diagrams): Nesse diretório está o [diagrama relacional](diagrams/DIAGRAMA_SISTEMAVOOS.pdf) (lógico) do sistema.
    * O sistema possui duas entidades: AERONAVES E VOOS
- [src](src): Nesse diretório estão os scripts do sistema
    * [conexion](src/conexion): Nesse repositório encontra-se o [módulo de conexão com o banco de dados Oracle](src/conexion/oracle_queries.py) e o [módulo de conexão com o banco de dados Mongo](src/conexion/mongo_queries.py). Esses módulos possuem algumas funcionalidades úteis para execução de instruções. O módulo do Oracle permite obter como resultado das queries JSON, Matriz e Pandas DataFrame. Já o módulo do Mongo apenas realiza a conexão, os métodos CRUD e de recuperação de dados são implementados diretamente nos objetos controladores (_Controllers_) e no objeto de Relatório (_reports_).
      - Exemplo de utilização para consultas simples no Oracle pelo MongoDB:

        ```python
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
        ```
      - Exemplo de utilização para alteração de registros no Oracle

        ```python
        from conexion.oracle_queries import OracleQueries
        def atualizar_aeronave(self) -> Aeronave:
          # Cria uma nova conexão com o banco que permite alteração
          self.mongo.connect()

          # Solicita ao usuario o novo codigo calda
          codigoCalda = (input("O código calda da aeronave que você deseja alterar: "))

          if not self.verifica_existencia_aeronave(codigoCalda):
            
            novo_nome = input("Nome (Novo): ")

            # Atualiza e persiste a nova aeronave
            self.mongo.db["TBL_AERONAVES"].update_one({"cd_calda": f"{codigoCalda}"}, {"$set": {"nm_aeronave": f"{novo_nome}"}})
           
            # Recupera os dados da nova aeronave criado transformando em um DataFrame
            df_aeronave = self.recuperar_aeronave(codigoCalda)
            
            # Cria um novo objeto Aeronave
            aeronave_atualizado = Aeronave(df_aeronave.cd_calda.values[0], df_aeronave.nm_aeronave.values[0])
           
             # Exibe os atributos da nova aeronave
            print(aeronave_atualizado.to_string())
            
            self.mongo.close()
            # Retorna o objeto aeronave_cliente para utilização posterior, caso necessário
            return aeronave_atualizado
          else:
            print(f"O Código calda {codigoCalda} não existe.")
            return None

      - Caso esteja utilizando na máquina virtual antiga, você precisará alterar o método connect de:
          
          ```python
          self.conn = cx_Oracle.connect(user=self.user,
                                  password=self.passwd,
                                  dsn=self.connectionString()
                                  )
          ```
        Para:
          ```python
          self.conn = cx_Oracle.connect(user=self.user,
                                  password=self.passwd,
                                  dsn=self.connectionString(in_container=True)
                                  )
          ```
      - Exemplo de utilização para conexão no Mongo;
      
      ```python
            # Importa o módulo MongoQueries
            from conexion.mongo_queries import MongoQueries
            
            # Cria o objeto MongoQueries
            mongo = MongoQueries()

            # Realiza a conexão com o Mongo
            mongo.connect()

            """<inclua aqui suas declarações>"""

            # Fecha a conexão com o Mong
            mongo.close()
      ```
      - Exemplo de criação de um documento no Mongo:
      
      ```python
        from conexion.mongo_queries import MongoQueries
        from model.aeronaves import Aeronave
        import pandas as pd
            
          def adicionar_aeronave(self) -> Aeronave:
            # Realiza a conexão com o Mongo
            self.mongo.connect()
            
            # Solicita ao usuario o codigo calda
            codigoCalda = input("Código calda: ")
            # Solicita ao usuario o nome da aeronave
            nomeAeronave = input("Nome: ")

            # Insere e persiste a nova aeronave
            self.mongo.db["TBL_AERONAVES"].insert_one({'cd_calda': codigoCalda, 'nm_aeronave': nomeAeronave})
            # Recupera os dados da nova aeronave criada transformando em um DataFrame
            df_aeronave = self.recuperar_aeronave(codigoCalda)
        
            nova_aeronave = Aeronave(df_aeronave.cd_calda.values[0], df_aeronave.nm_aeronave.values[0])

            # Exibe os dados da aeonave em formato DataFrame
            print(nova_aeronave.to_string())
            # Fecha a conexão com o Mong
            self.mongo.close()

            return nova_aeronave
      ```
    * [controller](src/controller/): Nesse diretório encontram-sem as classes controladoras, responsáveis por realizar inserção, alteração e exclusão dos registros das tabelas.
    * [model](src/model/): Nesse diretório encontram-ser as classes das entidades descritas no [diagrama relacional](diagrams/DIAGRAMA_SISTEMAVOOS.pdf)
    * [reports](src/reports/) Nesse diretório encontra-se a [classe](src/reports/relatorios.py) responsável por gerar todos os relatórios do sistema
    * [utils](src/utils/): Nesse diretório encontram-se scripts de [configuração](src/utils/config.py) e automatização da [tela de informações iniciais](src/utils/splash_screen.py)
    * [createCollectionsAndData.py](src/createCollectionsAndData.py): Script responsável por criar as coleções e registros fictícios. Esse script deve ser executado depois do script [create_tables_and_records.py](src/create_tables_and_records.py) para gerar as tabelas, caso não execute os scripts diretamente no MongoDB ou em alguma outra IDE de acesso ao Banco de Dados.
    * [principal.py](src/principal.py): Script responsável por ser a interface entre o usuário e os módulos de acesso ao Banco de Dados. Deve ser executado após a criação das tabelas.

### Bibliotecas Utilizadas
- [requirements.txt](src/requirements.txt): `pip install -r requirements.txt`