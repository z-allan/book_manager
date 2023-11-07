import streamlit as st
from models import Leitura
from services import Utilities
from datetime import datetime

class LeituraView:

    _util = Utilities()
    _user = None

    def __init__(self, p_usuario):
        self._user = p_usuario

    def incluir_view_leitura(self):
        """
            Monta a tela para gerenciamento de leituras.
            * Grid com todas as leituras, onde você pode selecionar alguma específica.
            * Incluir: formulário para incluir uma nova leitura.
            * Alterar: ao selecionar uma leitura na grid, é possível alterar as informações
            * Remover: ao selecionar uma leitura na grid, é possível remover

        Args:
            p_usuario (Object): recebe o usuário que será exibido as leituras
        """

        # variáveis globais para preencher combo box de livros e formatos, o usuário que está logado e se existe alguma editora selecionada
        global combo_livros, combo_formatos, p_max_data, p_min_data, selecionado, usuario_logado, tour_user
        
        # verifica se é usuário de Tour para desabilitar botões
        tour_user = self._user.perfil == 'Tour'

        # coloca o usuário que vem por parâmetro em uma váriavel para ser global
        usuario_logado = self._user
        
        # recebe o datafram que será usado para montar a grid com as leituras
        df = Leitura().montar_df_leitura(self._user)

        # monta o combo de livros e formatos que podem ser selecionados
        combo_livros = Leitura.buscar_livro_combo()
        combo_formatos = Leitura().lista_formatos
        
        # define a data minima e data maxima para inicio/fim de leitura
        p_max_data = datetime.now().date()
        p_min_data = datetime.strptime('1900-01-01','%Y-%m-%d')

        # caso o usuário não possua nenhuma leitura, mostra o formulário para inserir
        if df.size == 0:
            st.subheader('Incluir Leitura')
            self.adicionar_leitura()
        else:
            # monta a grid de leituras
            grid_resp = self._util.montar_grid(df, 'FIT_CONTENTS')
            selecionado = grid_resp['selected_rows']

            # verificar se possui alguma leitura em andamento, para adicionar uma observação
            pag = grid_resp['data']['Pag/Dia'].astype(str).str.contains('\*').any()
            dia = grid_resp['data']['Dias'].astype(str).str.contains('\*').any()
            if pag or dia:
                st.caption(f'\* Caso finalize a leitura hoje ({datetime.now().date().strftime("%d/%m/%y")})')

            # verifica se existe alguma mensagem de retorno por inserir/alterar/remover
            self._util.verificar_msg_retorno('Leitura')

            # caso existe alguma leitura selecionado na grid, habilita para editar/remover
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
                col1.subheader('Alterar Leitura')
                # botão remover leitura
                botao_remover = col2.button(label='Remover', disabled=tour_user)
                # ação ao clicar no botão remover
                if botao_remover:
                    leitura = Leitura(selecionado[0]['Id'],'','','',None,None,'','')
                    resultado = leitura.remover_leitura()
                    if resultado == None:
                        st.experimental_set_query_params(id='delok')
                        st.rerun()
                    else: 
                        st.error(resultado)
                # chama o form de alteração
                self.alterar_leitura()
            # caso não exista leitura selecionada, exibe o formulário para inserir
            else:
                st.subheader('Incluir Leitura')
                self.adicionar_leitura()
                    
    def adicionar_leitura(self):
        """
            Formulário para inserir uma nova leitura
        """

        # campos que serão apresentados para o usuário informar
        with st.form(key='incluir_leitura', clear_on_submit=True):
            ins_livro = st.selectbox('Livro:', combo_livros, index=0, disabled=tour_user)
            ins_formato = st.selectbox('Formato:', combo_formatos, index=1, disabled=tour_user)
            ins_coment = st.text_area(label='Comentário:', max_chars=500, value='', disabled=tour_user)
            # CSS para alinhar conteúdo do checkbox
            st.markdown("""
            <style>
                div[data-testid="stForm"] div[data-testid="column"]:nth-of-type(1) 
                {
                    flex: 0 0 150px;
                } 
                div[data-testid="stForm"] div[data-testid="column"]:nth-of-type(1) label
                {
                    padding: 20px 0;
                } 
            </style>
            """,unsafe_allow_html=True) 
            col1, col2 = st.columns(2)
            ins_check_ini = col1.checkbox('Iniciado', disabled=tour_user)
            ins_data_ini = col2.date_input('Data Iniciado: ', key='data_iniciado', help='A data só será levada em consideração caso o checkbox esteja selecionado', min_value=p_min_data, max_value=p_max_data, format='DD/MM/YYYY', disabled=tour_user)
            ins_check_fim = col1.checkbox('Finalizado', disabled=tour_user)
            ins_data_fim = col2.date_input('Data Finalizado:', key='data_finalizado', help='A data só será levada em consideração caso o checkbox esteja selecionado', min_value=p_min_data, max_value=p_max_data, format='DD/MM/YYYY', disabled=tour_user)
            botao_adicionar = st.form_submit_button(label='Adicionar', type='primary', disabled=tour_user)
        
        # ação que será executada ao dar submit no formulário
        if botao_adicionar:
            if ins_livro == '':
                st.warning('Favor escolher o livro.')
                st.stop()
            else:
                if not ins_check_ini:
                    ins_data_ini = None
                if not ins_check_fim:
                    ins_data_fim = None
                if ins_check_fim and not ins_check_ini:
                    ins_data_ini = ins_data_fim
                leitura = Leitura(0,usuario_logado.id,ins_livro,None,ins_data_ini,ins_data_fim,ins_formato,ins_coment)
                leitura.adicionar_leitura()
                st.experimental_set_query_params(id='insok')
                st.rerun()

    def alterar_leitura(self):
        """
            Formulário para alterar a leitura selecionada
        """
        p_combo_livros, p_combo_formato = Leitura().buscar_livro_selecionado(selecionado[0]['Id'])

        # campos que serão apresentado para o usuário alterar
        with st.form(key='alterar_leitura', clear_on_submit=True):
            upd_livro = st.selectbox('Livro:', combo_livros, index=p_combo_livros, disabled=tour_user)
            upd_formato = st.selectbox('Formato:', combo_formatos, index=p_combo_formato, disabled=tour_user)
            upd_coment = st.text_area(label='Comentário:', max_chars=500, value=selecionado[0]['Comentários'], disabled=tour_user)

            p_check_ini = True if selecionado[0]["Inicio Leitura"] != '' else False
            p_data_ini = datetime.strptime(selecionado[0]["Inicio Leitura"], '%d/%m/%Y').date() if selecionado[0]["Inicio Leitura"] != '' else datetime.now().date()
            
            p_check_fim = True if selecionado[0]["Fim Leitura"] != '' else False
            p_data_fim = datetime.strptime(selecionado[0]["Fim Leitura"], '%d/%m/%Y').date() if selecionado[0]["Fim Leitura"] != '' else datetime.now().date()

            # CSS para alinhar conteúdo do checkbox
            st.markdown("""
            <style>
                div[data-testid="stForm"] div[data-testid="column"]:nth-of-type(1) 
                {
                    flex: 0 0 150px;
                } 
                div[data-testid="stForm"] div[data-testid="column"]:nth-of-type(1) label
                {
                    padding: 20px 0;
                } 
            </style>
            """,unsafe_allow_html=True) 
            col1, col2 = st.columns(2)
            upd_check_ini = col1.checkbox('Iniciado',value=p_check_ini, disabled=tour_user)
            upd_data_ini = col2.date_input('Data Iniciado: ', key='data_iniciado', help='A data só será levada em consideração caso o checkbox esteja selecionado', value=p_data_ini, min_value=p_min_data, max_value=p_max_data, format='DD/MM/YYYY', disabled=tour_user)
            upd_check_fim = col1.checkbox('Finalizado',value=p_check_fim, disabled=tour_user)
            upd_data_fim = col2.date_input('Data Finalizado:', key='data_finalizado', help='A data só será levada em consideração caso o checkbox esteja selecionado', value=p_data_fim, min_value=p_min_data, max_value=p_max_data, format='DD/MM/YYYY', disabled=tour_user)
            
            botao_alterar = st.form_submit_button(label='Alterar', type='primary', disabled=tour_user)
        
        # ação que será executada ao dar submit no formulário
        if botao_alterar:
            if upd_livro == '':
                st.warning('Favor escolher o livro.')
                st.stop()
            else:
                if not upd_check_ini:
                    upd_data_ini = None
                if not upd_check_fim:
                    upd_data_fim = None
                if upd_check_fim and not upd_check_ini:
                    upd_data_ini = upd_data_fim

                leitura = Leitura(selecionado[0]['Id'],usuario_logado.id,upd_livro,None,upd_data_ini,upd_data_fim,upd_formato,upd_coment)
                leitura.alterar_leitura()
                st.experimental_set_query_params(id='updok')
                st.rerun()     