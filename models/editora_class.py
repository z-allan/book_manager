import pandas as pd
from controllers import EditoraController
from models import Log
from datetime import datetime

class Editora:

    _controller = None

    def __new__(cls, id=0, nome='', data_fund='1900-01-01', obs_editora=''):
        if cls._controller == None: 
            cls._controller = EditoraController()
        instance = super().__new__(cls)
        return instance

    def __init__(self, id=0, nome='', data_fund='1900-01-01', obs_editora=''):
        self.id = id
        self.nome = nome
        if isinstance(data_fund,str):
            self.data_fund = datetime.strptime(data_fund,'%Y-%m-%d') if data_fund != None else None
        else:
            self.data_fund = data_fund
        self.obs_editora = obs_editora
        
    def adicionar_editora(self):
        """
            Método utilizado para chamar a função que irá inserir a editora no banco de dados.

        Returns:
            String: se ocorreu erro ao inserir, será retornado uma mensagem.
        """
        resultado, value = self._controller.adicionar_editora_db(self)
        log_antes = self.dic_editora()
        self.id = value
        log_dps = self.dic_editora()
        if resultado:
            log = Log('editora','insert',log_antes, log_dps)
        else:
            log = Log('editora','insert',log_antes, value)
        log.adicionar_registro_log()
        return resultado, value

    def alterar_editora(self):
        """
            Método utilizado para chamar a função que irá alterar uma editora no banco de dados.
        """
        resp = self._controller.selecionar_editora_id_db(self.id)
        dado_atual = Editora(resp[0],resp[1],resp[2],resp[3])
        self._controller.alterar_editora_db(self)
        log_antes = dado_atual.dic_editora()
        log_depois = self.dic_editora()
        log = Log('editora','update',log_antes,log_depois)
        log.adicionar_registro_log()

    def remover_editora(self):
        """
            Método utilizado para chamar a função que irá remover uma editora do banco de dados.

        Returns:
            String: se ocorreu erro ao remover, será retornado uma mensagem.
        """
        resp = self._controller.selecionar_editora_id_db(self.id)
        dado_atual = Editora(resp[0],resp[1],resp[2],resp[3])
        resultado = self._controller.remover_editora_db(self)
        log_antes = dado_atual.dic_editora()
        if resultado == None:
            log = Log('editora','delete',log_antes)
        else:
            log = Log('editora','delete',log_antes,resultado)
        log.adicionar_registro_log()
        return resultado

    def __str__(self):
        """
            Método toString do objeto.

        Returns:
            String: retorna o nome como informação principal do objeto Editora.
        """
        return self.nome

    def __eq__(self, other):
        """
            Método utilizado para comparar 2 objetos do tipo Editora.

        Args:
            other (Object): objeto que será comparado

        Returns:
            bool: compara o nome, caso sejam iguais significa que são o mesmo objeto.
        """
        if not isinstance(other, Editora):
            return False
        return self.nome == other.nome

    def dic_editora(self):
        """
            Método para criar um dicionário com as informações que retornam do banco de dados.

        Returns:
            dict: dicionário com as informações que serão utilizadas para montar o grid.
        """

        if not isinstance(self.data_fund,str):
            self.data_fund = self.data_fund.strftime('%d/%m/%Y') if self.data_fund != None else ''

        return {'Nome': self.nome, 'Data Fundação': self.data_fund, 'Observação': self.obs_editora, 'Id': self.id}

    def montar_df_editora(self):
        """
            Método para criar um dataframe com os registros do banco de dados.
        
        Returns:
            DataFrame: dataframe com as informações das editoras.
        """
        resp = self._controller.selecionar_editoras_db()
        criar_editora = [Editora(row[0],row[1],row[2],row[3]) for row in resp]
        df = pd.DataFrame(
            [editora.dic_editora() for editora in criar_editora])
        return df
