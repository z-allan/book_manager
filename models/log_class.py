import streamlit as st
import pandas as pd
from datetime import datetime
import pytz
from controllers.log_controller import LogController

class Log:

    _controller = None

    def __new__(cls, tabela='', acao='', dado_antes='', dado_depois='', timestamp=None, id=0, usuario=None):
        if cls._controller == None:
            cls._controller = LogController()
        instance = super().__new__(cls)
        return instance

    def __init__(self, tabela='', acao='', dado_antes='', dado_depois='', timestamp=None, id=0, usuario=None):
        self.tabela = tabela
        self.acao = acao
        self.dado_antes = dado_antes
        self.dado_depois = dado_depois
        temp_data = datetime.now().astimezone(pytz.timezone('America/Sao_Paulo'))
        self.timestamp = temp_data if timestamp == None else timestamp
        self.id = id
        if usuario == None:
            self.usuario = st.session_state['agz_lib_user'].usuario_logado.login if 'agz_lib_user' in st.session_state else ''
        else:
            self.usuario = usuario
 
    def adicionar_registro_log(self):
        """
            Método utilizado para chamar a função que irá inserir o log no banco de dados.
        """
        self.montar_msg_log()
        self._controller.adicionar_registro_log_db(self)
    
    def montar_msg_log(self):
        """
            Método para montar a mensagem que será inserida no banco de dados
        """
        str_antes = ''
        str_depois = ''
        if isinstance(self.dado_antes,dict):
            for chave, valor in self.dado_antes.items():
                if str_antes == '':
                    str_antes += f"{chave}='{valor}'"
                else:
                    str_antes += f" | {chave}='{valor}'"
        else:
            str_antes = self.dado_antes
        if isinstance(self.dado_depois,dict):
            for chave, valor in self.dado_depois.items():
                if str_depois == '':
                    str_depois += f"{chave}='{valor}'"
                else:
                    str_depois += f" | {chave}='{valor}'"
        else:
            str_depois = self.dado_depois 
        self.dado_antes = str_antes
        self.dado_depois = str_depois

    def dic_log(self):
        """
            Método para criar um dicionário com as informações que retornam do banco de dados.

        Returns:
            dict: dicionário com as informações que serão utilizadas para montar o grid.
        """
        data = self.timestamp[:-6]
        if isinstance(data, str):
            data = datetime.strptime(data,'%Y-%m-%d %H:%M:%S.%f')
        return {'Data': data.strftime('%d/%m/%Y'), 'Hora': data.time(), 'Usuário': self.usuario, 'Tabela': self.tabela, 'Ação': self.acao, 'Antes':self.dado_antes, 'Depois':self.dado_depois,'Id': self.id}

    def montar_df_log(self, p_data_ini, p_data_fim):
        """
            Método para criar um dataframe com os registros do banco de dados.

        Args:
            p_data_ini (date): data inicial da pesquisa
            p_data_fim (date): data final da pesquisa

        Returns:
            DataFrame: dataframe com as informações de log.
        """
        criar_log = [Log(row[3],row[4],row[5],row[6],row[1],row[0],row[2]) for row in self._controller.selecionar_log_db(p_data_ini, p_data_fim)]
        df = pd.DataFrame([log.dic_log() for log in criar_log])
        return df

