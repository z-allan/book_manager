import streamlit as st
from models import Editora
from services import Utilities
from datetime import datetime

class EditoraView:

    _util = Utilities()
    _user = None

    def __init__(self, p_usuario):
        self._user = p_usuario

    def incluir_view_editora(self):
        """
            Monta a tela para gerenciamento de editoras.
            * Grid com todas as editoras, onde você pode selecionar alguma editora.
            * Incluir: formulário para incluir uma nova editora.
            * Alterar: ao selecionar uma editora na grid, é possível alterar as informações
            * Remover: ao selecionar uma editora na grid, é possível remover

        Args:
            p_usuario (Object): recebe o usuário que está logado para verificar o perfil
        """

        # variáveis globais para informar o perfil do usuário e se existe alguma editora selecionada
        global desabilitado, selecionado, tour_user
        
        # montar a grid das editoras
        teste = Editora(0,'',None,'')
        df_editora = teste.montar_df_editora()
        grid_resp = self._util.montar_grid(df_editora, 'FIT_ALL_COLUMNS_TO_VIEW')
        selecionado = grid_resp['selected_rows']

        # verifica o perfil do usuário
        # usuários do perfil admin e superuser pode inserir/alterar/remover editoras
        if self._user.perfil == 'Admin' or self._user.perfil == 'SuperUser':
            desabilitado = False
        else:
            desabilitado = True
        tour_user = self._user.perfil == 'Tour'

        # verifica se existe alguma mensagem de retorno por inserir/alterar/remover
        self._util.verificar_msg_retorno('Editora')

        # caso existe alguma editora selecionado na grid, habilita para editar/remover
        if selecionado: 
            # CSS para alinhar conteúdo a direita da tela
            st.markdown("""
            <style>
                div[data-testid="column"]:nth-of-type(2) 
                {
                    text-align: right;
                    align-self: end
                } 
            </style>
            """,unsafe_allow_html=True)   

            col1, col2 = st.columns(2)
            col1.subheader('Alterar Editora')
        
            # botão remover editora
            botao_remover = col2.button(label='Remover', disabled=desabilitado)
            # ação ao clicar no botão remover
            if botao_remover:
                editora = Editora(selecionado[0]['Id'],'',None,'')
                resultado = editora.remover_editora()
                if resultado == None:
                    st.experimental_set_query_params(id='delok')
                    st.rerun()
                else: 
                    st.error(resultado)

            self.alterar_editora()        
        # caso não exista editora selecionada, exibe o formulário para inserir
        else: 
            st.subheader('Incluir Editora')
            self.adicionar_editora()

            

    def adicionar_editora(self):
        """
            Formulário para inserir uma nova editora
        """

        # campos que serão apresentado para o usuário informar
        with st.form(key='incluir_editora', clear_on_submit=True):
            ins_nome = st.text_input(
                label='Nome Editora:',
                max_chars=100,
                value='', disabled=tour_user)
            # CSS para alinhar conteúdo do checkbox
            st.markdown("""
            <style>
                div[data-testid="stForm"] div[data-testid="column"]:nth-of-type(1) 
                {
                    flex: 0 0 275px;
                    align-self: center;
                } 
            </style>
            """,unsafe_allow_html=True) 
            col1, col2 = st.columns(2)
            ins_check_data = col1.checkbox('Sem informação de data', disabled=tour_user)
            ins_data = col2.date_input(
                label='Data Fundação:',
                #value=None,
                format='DD/MM/YYYY',
                help='Se o checkbox estiver selecionado, a data não será levada em consideração', disabled=tour_user)
            ins_obs = st.text_area(
                label='Observações:',
                max_chars=500,
                value='', disabled=tour_user)
            botao_adicionar = st.form_submit_button(label='Adicionar', disabled=tour_user, type='primary')

        # ação que será executada ao dar submit no formulário
        if botao_adicionar:
            if not ins_nome:
                st.warning('O nome da editora não pode estar vazio.')
                st.stop()
            else:
                if ins_check_data:
                    ins_data = None
                editora = Editora(0, ins_nome, ins_data, ins_obs)
                resultado, value = editora.adicionar_editora()
                if resultado:
                    st.experimental_set_query_params(id='insok')
                    st.rerun()
                else: 
                    st.error(value)

    def alterar_editora(self):
        """
            Formulário para alterar uma editora selecionada
        """
        p_data = datetime.strptime(selecionado[0]['Data Fundação'], '%d/%m/%Y').date() if selecionado[0]['Data Fundação'] != '' else datetime.now().date()
        p_obs = selecionado[0]['Observação'] if selecionado[0]['Observação'] != None else ''
        p_check = True if selecionado[0]['Data Fundação'] == '' else False

        # campos que serão apresentado para o usuário alterar
        # caso o usuário não tenha perfil, os campos estarão desabilitados
        with st.form(key='alterar_editora', clear_on_submit=True):
            upd_nome = st.text_input(
                label='Nome Editora:',
                max_chars=100,
                value=selecionado[0]['Nome'], disabled=desabilitado)
            st.markdown("""
            <style>
                div[data-testid="stForm"] div[data-testid="column"]:nth-of-type(1) 
                {
                    flex: 0 0 275px;
                    align-self: center;
                } 
            </style>
            """,unsafe_allow_html=True) 
            col1, col2 = st.columns(2)
            upd_check_data = col1.checkbox('Sem informação de data', value=p_check, disabled=desabilitado)
            upd_data = col2.date_input(
                label='Data Fundação:',
                value=p_data,
                format='DD/MM/YYYY',
                help='Se o checkbox estiver selecionado, a data não será levada em consideração', disabled=desabilitado)
            upd_obs = st.text_area(
                label='Observações:',
                max_chars=500,
                value=p_obs, disabled=desabilitado)
            botao_alterar = st.form_submit_button(label='Alterar', disabled=desabilitado, type='primary')
        
        # ação que será executada ao dar submit no formulário
        if botao_alterar:
            if not upd_nome:
                st.warning('O nome da editora não pode estar vazio.')
                st.stop()
            else:
                if upd_check_data:
                    upd_data = None
                editora = Editora(selecionado[0]['Id'], upd_nome, upd_data, upd_obs)
                editora.alterar_editora()
                st.experimental_set_query_params(id='updok')
                st.rerun()