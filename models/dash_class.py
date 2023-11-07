import pandas as pd
from controllers import DashController
from models import Livro, Autor, Editora, Leitura

class Dash:

    _controller = None

    def __new__(cls, leitura=None, livro=None, autor=None, editora=None):
        if cls._controller == None: 
            cls._controller = DashController()
        instance = super().__new__(cls)
        return instance
    
    def __init__(self, leitura=None, livro=None, autor=None, editora=None):
        self.leitura = leitura
        self.livro = livro
        self.autor = autor
        self.editora = editora

    def dic_dash(self):
        """
            Método para criar um dicionário com as informações que retornam do banco de dados.

        Returns:
            dict: dicionário com as informações que serão utilizadas para montar os gráficos.
        """
        if isinstance(self.leitura.pag_dia,str):
            self.leitura.pag_dia = 0
        if isinstance(self.leitura.tempo,str):
            self.leitura.tempo = 0

        self.leitura.data_ini = self.leitura.data_ini.strftime('%d/%m/%Y') if self.leitura.data_ini != None else ''
        self.leitura.data_fim = self.leitura.data_fim.strftime('%d/%m/%Y') if self.leitura.data_fim != None else ''
        self.editora.data_fund = self.editora.data_fund.strftime('%d/%m/%Y') if self.editora.data_fund != None else ''

        return {'id_usuario': self.leitura.usuario, 'id_leitura': self.leitura.id, 'data_ins': self.leitura.data_ins, 'data_ini': self.leitura.data_ini, 'data_fim': self.leitura.data_fim, 'formato': self.leitura.formato, 'obs_leitura': self.leitura.coment_livro, 'pag_dia': self.leitura.pag_dia, 'total_dias': self.leitura.tempo , 'ano_ini': self.leitura.ano_ini, 'ano_fim': self.leitura.ano_fim, 'mes_ini': self.leitura.mes_ini, 'mes_fim': self.leitura.mes_fim, 'id_livro': self.livro.id, 'nome_livro': self.livro.nome, 'num_edicao': self.livro.edicao, 'num_pag': self.livro.num_pag, 'obs_livro': self.livro.obs_livro, 'livro_autor': self.livro.autor, 'livro_editora': self.livro.editora, 'id_autor': self.autor.id, 'nome_autor': self.autor.nome_real, 'pseud_autor': self.autor.pseudonimo, 'ano_nasc': self.autor.ano_nasc, 'ano_morte': self.autor.ano_morte, 'local': self.autor.local_nasc, 'obs_autor': self.autor.obs_autor, 'id_editora': self.editora.id, 'nome_editora': self.editora.nome, 'data_criacao': self.editora.data_fund, 'obs_editora': self.editora.obs_editora}

    def montar_df_usuario_dash(self, p_usuario):
        """
            Método para criar um dataframe com os registros do banco de dados.

        Args:
            p_usuario (Object): usuário que será utilizado na consulta

        Returns:
            DataFrame: dataframe com as informações de leituras de determinado usuário.
        """
        resp = self._controller.selecionar_usuario_dash_db(p_usuario)
        temp_list = []
        for row in resp:
            livro = Livro(row[6],row[7],row[8],row[9],row[10],row[11],row[18])
            leitura = Leitura(row[0],p_usuario.id,livro,row[1],row[2],row[3],row[4],row[5])
            autor = Autor(row[11],row[12],row[13],row[14],row[15],row[16],row[17])
            editora = Editora(row[18],row[19],row[20],row[21])
            temp_list.append(Dash(leitura,livro,autor,editora))
        
        df = pd.DataFrame([dash.dic_dash() for dash in temp_list])
        return df
    
    def montar_df_total_dash(self):
        """
            Método para criar um dataframe com os registros do banco de dados.

        Returns:
            DataFrame: dataframe com as informações de leituras de todos usuários.
        """
        resp = self._controller.selecionar_total_dash_db()
        temp_list = []
        for row in resp:
            livro = Livro(row[6],row[7],row[8],row[9],row[10],row[11],row[18])
            leitura = Leitura(row[0],row[22],livro,row[1],row[2],row[3],row[4],row[5])
            autor = Autor(row[11],row[12],row[13],row[14],row[15],row[16],row[17])
            editora = Editora(row[18],row[19],row[20],row[21])
            temp_list.append(Dash(leitura,livro,autor,editora))
        df = pd.DataFrame(
            [dash.dic_dash() for dash in temp_list])
        return df