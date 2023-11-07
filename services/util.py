import streamlit as st
from streamlit_option_menu import option_menu
from st_aggrid import AgGrid, GridOptionsBuilder

class Utilities:

    def montar_menu_main(self, p_opcoes):
        """
            Monta o menu principal que fica no canto esquerdo da tela (sidebar)

        Args:
            p_opcoes (dict): recebe um dicionario onde as chaves são os icones (bootstrap icons) e os valores são as opções que podem ser selecionadas

        Returns:
            String: retorna a opção que está selecionada
        """
        with st.sidebar:
            return option_menu(
                menu_title='Biblioteca',
                menu_icon='server',
                options=list(p_opcoes.values()),
                icons=list(p_opcoes.keys()),
                default_index=int(st.session_state['selected_menu']),
                orientation="vertical",
                styles={
                    "container": {"padding": "0!important"},
                    "icon": {"color": "#D9B282", "font-size": "1em"},
                    "nav-link": {"font-size": "1.1em", "text-align": "left", "margin": "0px"},
                    "nav-link-selected": {"font-weight": "normal"},
                })

    def montar_menu_dash(self, p_opcoes):
        """
            Monta o menu que fica na parte superior da tela Dashboard.

        Args:
            p_opcoes (dict): recebe um dicionario onde as chaves são os icones (bootstrap icons) e os valores são as opções que podem ser selecionadas

        Returns:
            String: retorna a opção que está selecionada
        """
        return option_menu(
            menu_title=None,
            options=list(p_opcoes.values()),
            icons=list(p_opcoes.keys()),
            default_index=0,
            orientation="horizontal",
            styles={
                "container": {"padding": "0!important"},
                "icon": {"color": "#D9B282", "font-size": "1em"},
                "nav-link": {"font-size": "1.1em", "text-align": "center", "margin": "0px"},
                "nav-link-selected": {"font-weight": "normal"},
            })

    def montar_menu_usuario(self, p_opcoes):
        """
            Monta o menu que fica abaixo da grid de usuário quando não existe nenhum usuário selecionado.

        Args:
            p_opcoes (dict): recebe um dicionario onde as chaves são os icones (bootstrap icons) e os valores são as opções que podem ser selecionadas

        Returns:
            String: retorna a opção que está selecionada
        """
        return option_menu(
            menu_title='',
            options=list(p_opcoes.values()),
            icons=list(p_opcoes.keys()),
            orientation="horizontal",
            styles={
                "container": {"padding": "0!important"},
                "icon": {"color": "#D9B282", "font-size": "1em"},
                "nav-link": {"font-size": "1.1em", "text-align": "center", "margin": "0px"},
                "nav-link-selected": {"font-weight": "normal"},
            })

    def montar_grid(self, p_df, p_size):
        """
            Função utilizada para configurar as opções que serão utilizadas no st_aggrid e criar a a grid.

        Args:
            p_df (DataFrame): recebe o DataFrame que será utilizado para montar a grid.
            p_size (String): recebe a informção do auto_size das colunas da grid.

        Returns:
            AgGrid: tabela com os dados num formato mais personalizado.
        """
        build = GridOptionsBuilder.from_dataframe(p_df)
        build.configure_column(field='Id', header_name='Id', hide=True)
        # build.configure_column(field='Observação', header_name='Observação',hide=True)
        build.configure_selection(selection_mode='single', use_checkbox=True,
                                suppressRowClickSelection=False, suppressRowDeselection=True)
        build.configure_pagination(enabled=True, paginationAutoPageSize=False, paginationPageSize=12)
        build.configure_default_column(sortable=False)
        #build.configure_auto_height(autoHeight=False)
        go = build.build()

        grid = AgGrid(
                    # altera o estilo da ferramente de quicksearch
                    custom_css={
                                "#gridToolBar input": {
                                    "font-size": "1.15em",
                                    "height": "30px",
                                    "margin": "0 !important",
                                    "padding-left": "10px"
                                }
                             },
                    data=p_df,
                    columns_auto_size_mode=p_size,
                    gridOptions=go,
                    enable_quicksearch=True,
                    enable_enterprise_modules=False)
        
        # força a altura do iframe, pois a paginação ficava cortada quando abria pela primeira vez
        st.markdown("""
            <style>
                iframe[title="st_aggrid.agGrid"] 
                {
                    height: 450px;
                } 
            </style>
            """,unsafe_allow_html=True) 

        return grid


    def verificar_msg_retorno(self, p_model):
        """
            Função utilizada para mostrar mensagem de sucesso após a tela ser atualizada ao realizar insert/update/delete de registros.

        Args:
            p_model (String): qual classe está executando a função
        """
        letra_final = 'a' if p_model == 'Editora' or p_model == 'Leitura' else 'o'

        get = st.experimental_get_query_params()
        if get != {}:
            if 'id' in get:
                # CSS para alinhar botão e mensagem de sucesso
                st.markdown("""
                <style>
                    div[data-testid="column"]:nth-of-type(1) 
                    {
                        align-self: center;
                        flex: 0 1 55px
                    } 
                </style>
                """,unsafe_allow_html=True) 
                #col1, col2 = st.columns(2)
                #col1.button('OK')
                if get['id'][0] == 'insok':
                    st.toast(f'{p_model} adicionad{letra_final} com sucesso.', icon="✅")
                elif get['id'][0] == 'updok':
                    st.toast(f'{p_model} alterad{letra_final} com sucesso.', icon="✅")
                elif get['id'][0] == 'delok':
                    st.toast(f'{p_model} removid{letra_final} com sucesso.', icon="✅")
                del get['id']
                st.markdown("""
                <style>
                    div[data-baseweb="toast"]
                    {
                        background-color: #CCFFCC;
                    } 
                </style>
                """,unsafe_allow_html=True) 
                st.experimental_set_query_params(query_params=get)
