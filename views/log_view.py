import streamlit as st
from datetime import datetime, timedelta
from models import Log
from services.util import Utilities

class LogView:

    _util = Utilities()

    def incluir_view_log(self):
        data_ini = None
        data_fim = None
        opcoes = ('Hoje', '7 dias', '15 dias', '30 dias', 'Outra data')
        opcao_selecionada = 0
        datas_selecionadas = []

        if 'agzlog_opcao' in st.session_state:
            opcao_selecionada = opcoes.index(st.session_state['agzlog_opcao'])
            datas_selecionadas = [st.session_state['agzlog_ini'], st.session_state['agzlog_fim']]
        
        col1, col2 = st.columns((1,1))
        log_selecionado = col1.selectbox('Buscar log:', opcoes, index=opcao_selecionada, on_change=self.opcao_alterada)

        data_ini = datetime.now().date()
        data_fim = datetime.now().date()

        if log_selecionado == '7 dias':
            data_ini = datetime.now().date() - timedelta(days=6)
        elif log_selecionado == '15 dias':
            data_ini = datetime.now().date() - timedelta(days=14)
        elif log_selecionado == '30 dias':
            data_ini = datetime.now().date() - timedelta(days=29)
        elif log_selecionado == 'Outra data':
            range_datas = col2.date_input('Escolha as datas:', datas_selecionadas)
            if len(range_datas) != 0:
                data_ini = range_datas[0]
                if len(range_datas) > 1:
                    data_fim = range_datas[1]
                else:
                    data_fim = range_datas[0]
        
        diferenca_dias = data_fim - data_ini
        botao_desabilitado = False
        selecionado = None

        if diferenca_dias.days > 60:
            st.warning('Não é possível realizar pesquisas com mais de 60 dias.')
            botao_desabilitado = True
        
        if st.button('Pesquisar', disabled=botao_desabilitado, type='primary'):
            st.session_state['agzlog_opcao'] = log_selecionado
            st.session_state['agzlog_ini'] = data_ini
            st.session_state['agzlog_fim'] = data_fim
        
        if 'agzlog_opcao' in st.session_state:
            st.code(f"Data Inicial: {data_ini.strftime('%d/%m/%Y')} | Data Final: {data_fim.strftime('%d/%m/%Y')} | Dias: {diferenca_dias.days + 1}")
            data_ini = st.session_state['agzlog_ini']
            data_fim = st.session_state['agzlog_fim']
            df_log = Log().montar_df_log(data_ini, data_fim)
            grid_resp = self._util.montar_grid(df_log, 'FIT_CONTENTS')
            selecionado = grid_resp['selected_rows']

            if selecionado:
                st.write('Informações')
                st.code(f"{selecionado[0]['Data']} {selecionado[0]['Hora']} - {selecionado[0]['Usuário']} - {selecionado[0]['Tabela']} - {selecionado[0]['Ação']}")
                st.write('Antes')
                st.code(selecionado[0]['Antes'].replace(' | ', '\n'))
                st.write('Depois')
                st.code(selecionado[0]['Depois'].replace(' | ', '\n'))    
                

    def opcao_alterada(self):
        if 'agzlog_opcao' in st.session_state:
            del st.session_state['agzlog_opcao']
            del st.session_state['agzlog_ini']
            del st.session_state['agzlog_fim']

    
    