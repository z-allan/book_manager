import streamlit as st
from models import Autor
from services import Utilities
from datetime import datetime

class AutorView:

    _util = Utilities()
    _user = None

    def __init__(self, p_usuario):
        self._user = p_usuario

    def incluir_view_autor(self):
        """
            Monta a tela para gerenciamento de autores.
            * Grid com todos os autores, onde você pode selecionar algum autor.
            * Incluir: formulário para incluir um novo autor.
            * Alterar: ao selecionar um autor na grid, é possível alterar as informações
            * Remover: ao selecionar um autor na grid, é possível remover

        Args:
            p_usuario (Object): recebe o usuário que está logado para verificar o perfil
        """

        # variáveis globais para informar o perfil do autor e se existe algum autor selecionado
        global desabilitado, selecionado, tour_user
        
        # montar a grid dos autores
        df_autor = Autor().montar_df_autor()
        grid_resp = self._util.montar_grid(df_autor, 'FIT_ALL_COLUMNS_TO_VIEW')
        selecionado = grid_resp['selected_rows']
        
        # verifica o perfil do usuário
        # usuários do perfil admin e superuser pode inserir/alterar/remover autores
        if self._user.perfil == 'Admin' or self._user.perfil == 'SuperUser':
            desabilitado = False
        else:
            desabilitado = True
        tour_user = self._user.perfil == 'Tour'

        # verifica se existe alguma mensagem de retorno por inserir/alterar/remover
        self._util.verificar_msg_retorno('Autor')

        # caso existe algum autor selecionado na grid, habilita para editar/remover
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
            col1.subheader('Alterar Autor')

            # botão de remover autor
            botao_remover = col2.button(label='Remover', disabled=desabilitado)
            # ação ao clicar no botão remover
            if botao_remover:
                autor = Autor(selecionado[0]['Id'],'','','','','','')
                resultado = autor.remover_autor()
                if resultado == None:
                    st.experimental_set_query_params(id='delok')
                    st.rerun()
                else: 
                    st.error(resultado)
            
            self.alterar_autor()   
        # caso não exista autor selecionado, exibe o formulário para inserir
        else:
            st.subheader('Incluir Autor')
            self.adicionar_autor()

    def adicionar_autor(self):
        """
            Formulário para inserir um novo autor
        """

        # campos que serão apresentado para o usuário informar
        with st.form(key='incluir_autor', clear_on_submit=True):
            ins_pseudonimo = st.text_input(label='Pseudonimo:', max_chars=200, value='', disabled=tour_user)
            ins_nome = st.text_input(label='Nome Autor:', max_chars=200, value='', disabled=tour_user)
            col1, col2 = st.columns((1,1))
            ins_nasc = col1.number_input(label='Ano Nascimento:', min_value=-9999, max_value=datetime.now().year, value=0, disabled=tour_user)
            ins_morte = col2.number_input(label='Ano Morte:', min_value=-9999, max_value=datetime.now().year, value=0, disabled=tour_user)
            ins_local = st.text_input(label='Local Nascimento:', max_chars=200, disabled=tour_user)
            ins_obs = st.text_area(label='Observações:', max_chars=500, value='', disabled=tour_user)
            botao_adicionar = st.form_submit_button(label='Adicionar', disabled=tour_user, type='primary')
        
        # ação que será executada ao dar submit no formulário
        if botao_adicionar:
            if not ins_pseudonimo:
                st.warning('O pseudonomio do autor não pode estar vazio.')
                st.stop()
            else:
                if ins_nasc == 0:
                    ins_nasc = ''
                if ins_morte == 0:
                    ins_morte = ''

                autor = Autor(0,ins_nome,ins_pseudonimo,ins_nasc,ins_morte,ins_local,ins_obs)
                resultado, value = autor.adicionar_autor()
                
                if resultado:
                    st.experimental_set_query_params(id='insok')
                    st.rerun()
                else: 
                    st.error(value)

    def alterar_autor(self):
        """
            Formulário para alterar um autor selecionado
        """
        p_obs = selecionado[0]['Observação'] if selecionado[0]['Observação'] != None else ''
        p_nasc = selecionado[0]['Ano Nascimento'] if selecionado[0]['Ano Nascimento'] != '' else 0
        p_morte = selecionado[0]['Ano Morte'] if selecionado[0]['Ano Morte'] != '' else 0

        # campos que serão apresentado para o usuário alterar
        # caso o usuário não tenha perfil, os campos estarão desabilitados
        with st.form(key='alterar_autor', clear_on_submit=True):
            upd_pseudonimo = st.text_input(label='Pseudonimo:', max_chars=200, value=selecionado[0]['Pseudonimo'], disabled=desabilitado)
            upd_nome = st.text_input(label='Nome Autor:', max_chars=200, value=selecionado[0]['Nome'], disabled=desabilitado)            
            
            col1, col2 = st.columns((1,1))
            upd_nasc = col1.number_input(label='Ano Nascimento:', min_value=-9999, max_value=datetime.now().year, value=int(p_nasc), disabled=desabilitado)
            upd_morte = col2.number_input(label='Ano Morte:', min_value=-9999, max_value=datetime.now().year, value=int(p_morte), disabled=desabilitado)
            
            upd_local = st.text_input(label='Local Nascimento:', max_chars=200, value=selecionado[0]['Local Nascimento'], disabled=desabilitado)
            upd_obs = st.text_area(label='Observações:', max_chars=500, value=p_obs, disabled=desabilitado)
            botao_alterar = st.form_submit_button(label='Alterar', disabled=desabilitado, type='primary')

        # ação que será executada ao dar submit no formulário
        if botao_alterar:
            if not upd_pseudonimo:
                st.warning('O pseudonomio do autor não pode estar vazio.')
                st.stop()
            else:
                if upd_nasc == 0:
                    upd_nasc = ''
                if upd_morte == 0:
                    upd_morte = ''

                autor = Autor(selecionado[0]['Id'],upd_nome,upd_pseudonimo,upd_nasc,upd_morte,upd_local,upd_obs)
                autor.alterar_autor()
                st.experimental_set_query_params(id='updok')
                st.rerun()