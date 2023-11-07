import streamlit as st
import pandas as pd
import pytz
from models import Log, Livro
from controllers import LeituraController
from datetime import datetime

class Leitura:

    lista_formatos = ['Ebook', 'Físico', 'PDF']
    _controller = None

    def __new__(cls, id=0, usuario=None, livro=None, data_ins=None, data_ini=None, data_fim=None, formato='', coment_livro=''):
        if cls._controller == None:
            cls._controller = LeituraController()
        instance = super().__new__(cls)
        return instance    

    def __init__(self, id=0, usuario=None, livro=None, data_ins=None, data_ini=None, data_fim=None, formato='', coment_livro=''):
        self.id = id
        self.usuario = usuario
        self.livro = livro
        self.data_ins = datetime.now().astimezone(pytz.timezone('America/Sao_Paulo')).strftime("%Y-%m-%dT%H:%M:%S.%f") if data_ins == None else data_ins
        if (isinstance(data_ini,str)):
            self.data_ini = datetime.strptime(data_ini, '%Y-%m-%d').date()
        else:
            self.data_ini = data_ini
        if (isinstance(data_fim,str)):
            self.data_fim = datetime.strptime(data_fim, '%Y-%m-%d').date()
        else:
            self.data_fim = data_fim
        self.formato = formato
        self.coment_livro = coment_livro
        self.pag_dia = self.pag_lida_dia()
        self.tempo = self.total_dias()
        self.ano_ini = self.data_ini.year if data_ini != None else ''
        self.ano_fim = self.data_fim.year if data_fim != None else ''
        self.mes_ini = self.data_ini.month if data_ini != None else ''
        self.mes_fim = self.data_fim.month if data_fim != None else ''

    def pag_lida_dia(self):
        """
            Método utilizado para calcular a quantidade de páginas lidas por dia.

        Returns:
            String: retorna a quantidade de páginas (pode contar uma observação *)
        """
        qtd_pag = ''
        if self.data_ini != None and self.data_fim != None:
            dias = (self.data_fim-self.data_ini).days
            qtd_pag = round(self.livro.num_pag/dias, 0) if dias > 0 else self.livro.num_pag
        elif self.data_ini != None and self.data_ini != datetime.now().date():
            if self.data_fim == None:
                qtd_pag = f'{round(self.livro.num_pag/(datetime.now().date()-self.data_ini).days)}*'
        return qtd_pag

    def total_dias(self):
        """
            Método utilizado para calcular quantos dias de leitura.

        Returns:
            String: retorna a quantidade de dias (pode contar uma observação *)
        """
        qt_dia = ''
        if self.data_ini != None and self.data_fim != None:
            qt_dia = (self.data_fim-self.data_ini).days
        elif self.data_ini != None:
            if self.data_fim == None:
                qt_dia = f'{(datetime.now().date()-self.data_ini).days}*'
        return qt_dia

    def adicionar_leitura(self):
        """
            Método para chamar a função que irá inserir a leitura no banco de dados.
        """
        log_antes = self.dic_leitura()
        if isinstance(self.data_ini,str):
            if self.data_ini == '':
                self.data_ini = None
            else:
                self.data_ini = datetime.strptime(self.data_ini, '%d/%m/%Y').date()
        if isinstance(self.data_fim,str):
            if self.data_fim == '':
                self.data_fim = None
            else:
                self.data_fim = datetime.strptime(self.data_fim, '%d/%m/%Y').date()
        st.write(self.data_ini)
        self.id = self._controller.adicionar_leitura_db(self)
        log_dps = self.dic_leitura()
        log = Log('leitura','insert',log_antes,log_dps)
        log.adicionar_registro_log()

    def alterar_leitura(self):
        """
            Método para chamar a função que irá alterar uma leitura no banco de dados.
        """
        row = self._controller.selecionar_leitura_id_db(self.id)
        dado_atual = Leitura(row[0],row[1],Livro(row[8],row[9],row[11],row[12],row[13],'',''),row[3],row[4],row[5],row[6],row[7])
        self._controller.alterar_leitura_db(self)
        log_antes = dado_atual.dic_leitura()
        self.data_ins = dado_atual.data_ins
        log_dps = self.dic_leitura()
        log = Log('leitura','update',log_antes,log_dps)
        log.adicionar_registro_log()

    def remover_leitura(self):
        """
            Método para chamar a função que irá remover uma leitura no banco de dados.
        """
        row = self._controller.selecionar_leitura_id_db(self.id)
        dado_atual = Leitura(row[0],row[1],Livro(row[8],row[9],row[11],row[12],row[13],'',''),row[3],row[4],row[5],row[6],row[7])
        self._controller.remover_leitura_db(self)
        log_antes = dado_atual.dic_leitura()
        log = Log('leitura','delete',log_antes)
        log.adicionar_registro_log()

    def buscar_livro_combo():
        """
            Método para popular o combo box de livros que podem ser selecionado para leitura.

            * Insere um registro em branco para ser melhor visualizado na tela.

        Returns:
            list: uma lista de objetos da classe Livro.
        """
        return [''] + Livro().selecionar_livros()

    def buscar_livro_selecionado(self, p_id):
        """
            Método para verificar o index de determinado livro e determido formato de uma leitura que foi selecionada na grid para popular corretamente o combo box.

        Args:
            p_id (int): id da leitura que foi selecionada

        Returns:
            int: o index do livro e o index da leitura.
        """
        row = self._controller.selecionar_leitura_id_db(p_id)
        leitura_selecionada = Leitura(row[0],row[1],Livro(row[8],row[9],row[11],row[12],row[13],'',''),row[3],row[4],row[5],row[6],row[7])        
        return Livro().selecionar_livros().index(leitura_selecionada.livro)+1, Leitura.lista_formatos.index(leitura_selecionada.formato)

    def dic_leitura(self):
        """
            Método para criar um dicionário com as informações que retornam do banco de dados.

        Returns:
            dict: dicionário com as informações que serão utilizadas para montar o grid.
        """
        if not isinstance(self.data_ini,str):
            self.data_ini = self.data_ini.strftime('%d/%m/%Y') if self.data_ini != None else ''
        if not isinstance(self.data_fim,str):
            self.data_fim = self.data_fim.strftime('%d/%m/%Y') if self.data_fim != None else ''
        if not isinstance(self.data_ins,str):
            self.data_ins = self.data_ins.strftime('%d/%m/%Y %H:%M:%S') if self.data_ins != None else ''

        return {'Ano': self.ano_ini, 'Nome': self.livro.nome, 'Inicio Leitura': self.data_ini, 'Fim Leitura': self.data_fim, 'Pag/Dia': self.pag_dia, 'Dias': self.tempo, 'Formato Livro': self.formato, 'Comentários': self.coment_livro, 'Data Inserção': self.data_ins, 'Id': self.id}

    def montar_df_leitura(self, p_usuario):
        """
            Método para criar um dataframe com os registros do banco de dados.
        
        Returns:
            DataFrame: dataframe com as informações das leituras.
        """
        resp = self._controller.selecionar_leituras_db(p_usuario)
        criar_leitura = [Leitura(row[0],row[1],Livro(row[8],row[9],row[11],row[12],row[13],'',''),row[3],row[4],row[5],row[6],row[7]) for row in resp]
        df = pd.DataFrame(
            [leitura.dic_leitura() for leitura in criar_leitura])
        return df
    
    
