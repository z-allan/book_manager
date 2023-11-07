import streamlit as st
from models import Livro
from services import Utilities

class LivroView:

    _util = Utilities()
    _user = None

    def __init__(self, p_usuario):
        self._user = p_usuario

    def incluir_view_livro(self):
        """
            Monta a tela para gerenciamento de livros.
            * Grid com todos os livros, onde você pode selecionar algum livros.
            * Incluir: formulário para incluir um novo livros.
            * Alterar: ao selecionar um livros na grid, é possível alterar as informações
            * Remover: ao selecionar um livros na grid, é possível remover

        Args:
            p_usuario (Object): recebe o usuário que está logado para verificar o perfil
        """

        # variáveis globais para preencher combo box de autores e editora, o perfil do usuário que está logado e se existe algum livro selecionada
        global combo_editoras, multi_autores, desabilitado, tour_user, selecionado

        # montar a grid dos livros
        df_livro = Livro().montar_df_livro()
        grid_resp = self._util.montar_grid(df_livro, 'FIT_ALL_COLUMNS_TO_VIEW')
        selecionado = grid_resp['selected_rows']
        
        # verifica o perfil do usuário
        # usuários do perfil admin e superuser pode inserir/alterar/remover livros
        if self._user.perfil == 'Admin' or self._user.perfil == 'SuperUser':
            desabilitado = False
        else:
            desabilitado = True
        tour_user = self._user.perfil == 'Tour'

        # verifica se existe alguma mensagem de retorno por inserir/alterar/remover
        self._util.verificar_msg_retorno('Livro')

        # monta o combo box de editoras e o multi select de autores
        combo_editoras = Livro().busca_editora_combo()
        multi_autores = Livro().busca_autores_multi()

        # caso existe algum livro selecionado na grid, habilita para editar/remover
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
            col1.subheader('Alterar Livro')
            # botão de remover livro
            botao_remover = col2.button(label='Remover', disabled=desabilitado)
            # ação ao clicar no botão remover
            if botao_remover:
                livro = Livro(selecionado[0]['Id'],'','','','','','')
                resultado = livro.remover_livro()
                if resultado == None:
                    st.experimental_set_query_params(id='delok')
                    st.rerun()
                else: 
                    st.error(resultado)
            # chama o form de alteração
            self.alterar_livro()        
        # caso não exista livro selecionado, exibe o formulário para inserir
        else:
            st.subheader('Incluir Livro')
            self.adicionar_livro()

            

    def adicionar_livro(self):
        """
            Formulário para inserir um novo livro
        """

        # campos que serão apresentado para o usuário informar
        with st.form(key='incluir_Livro', clear_on_submit=True):
            ins_nome = st.text_input(label='Nome do Livro:', max_chars=200, value='', disabled=tour_user)
            ins_autores = st.multiselect('Autores', multi_autores, disabled=tour_user)
            col1, col2, col3 = st.columns((4,2,2))
            ins_editora = col1.selectbox('Editora', combo_editoras, index=0, disabled=tour_user)
            ins_edicao = col2.number_input(label='Edição:', min_value=1, max_value=999, value=1, disabled=tour_user)
            ins_pag = col3.number_input(label='Número de Páginas:', min_value=1, max_value=9999, value=250, disabled=tour_user)
            ins_obs = st.text_area(label='Observações:', max_chars=500, value='', disabled=tour_user)
            botao_adicionar = st.form_submit_button(label='Adicionar', disabled=tour_user, type='primary')
        
        # ação que será executada ao dar submit no formulário
        if botao_adicionar:
            if not ins_nome:
                st.warning('O nome do livro não pode estar vazio.')
                st.stop()
            elif not ins_autores:
                st.warning('O livro precisa ter pelo meno 1 autor.')
                st.stop()
            elif ins_editora == '':
                st.warning('Favor escolher a editora.')
                st.stop()
            else:
                livro = Livro(0,ins_nome,ins_edicao,ins_pag,ins_obs,ins_autores,ins_editora)
                resultado = livro.adicionar_livro()
                if resultado == None:
                    st.experimental_set_query_params(id='insok')
                    st.rerun()
                else:
                    st.error(resultado)

    def alterar_livro(self):
        """
            Formulário para alterar um livro selecionado
        """
        p_combo_editoras = Livro().busca_editora_selecionada(str(selecionado[0]['Editora']))
        p_multi_autores = Livro().busca_autores_selecionado(str(selecionado[0]['Autores']).split(', '))
        p_obs = selecionado[0]['Observação'] if selecionado[0]['Observação'] != None else ''

        # campos que serão apresentado para o usuário alterar
        # caso o usuário não tenha perfil, os campos estarão desabilitados
        with st.form(key='alterar_Livro', clear_on_submit=True):
            upd_nome = st.text_input(label='Nome do Livro:', max_chars=200, value=selecionado[0]['Nome'], disabled=desabilitado)
            upd_autores = st.multiselect('Autores', options=multi_autores, default=p_multi_autores, disabled=desabilitado)
            col1, col2, col3 = st.columns((4,2,2))
            upd_editora = col1.selectbox('Editora', options=combo_editoras, index=p_combo_editoras, disabled=desabilitado)
            upd_edicao = col2.number_input(label='Edição:', min_value=1, max_value=999, value=selecionado[0]['Edicao'], disabled=desabilitado)
            upd_pag = col3.number_input(label='Número de Páginas:', min_value=1, max_value=9999, value=selecionado[0]['Nº Paginas'], disabled=desabilitado)
            upd_obs = st.text_area(label='Observações:', max_chars=500, value=p_obs)
            botao_alterar = st.form_submit_button(label='Alterar', disabled=desabilitado, type='primary')
        
        # ação que será executada ao dar submit no formulário
        if botao_alterar:
            if not upd_nome:
                st.warning('O nome do livro não pode estar vazio.')
                st.stop()
            elif not upd_autores:
                st.warning('O livro precisa ter pelo meno 1 autor.')
                st.stop()
            elif upd_editora == '':
                st.warning('Favor escolher a editora.')
                st.stop()
            else:
                livro = Livro(selecionado[0]['Id'],upd_nome,upd_edicao,upd_pag,upd_obs,upd_autores,upd_editora)
                livro.alterar_livro()
                st.experimental_set_query_params(id='updok')
                st.rerun()