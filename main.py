import streamlit as st
# configuração iniciais do streamlit
st.set_page_config(page_title='Biblioteca',page_icon='book',initial_sidebar_state="expanded",menu_items={'Get help': 'https://github.com/z-allan/','About': "https://z-allan.github.io/site"})
from services import Utilities
from views import *

# dicionario com as opções que serão exibidas no menu principal
opcoes_main = {'graph-up-arrow':'Dashboard',
               'table':'Leitura',
               's1':'---',
               'book':'Livros', 
               'people':'Autores', 
               'building':'Editoras', 
               's2':'---',
               'person':'Usuários'}

# caso já existe uma sessão, adicionamos opções no menu
if 'agz_lib_user' in st.session_state: 
    # varíavel recebe o objeto usuário da sessão
    usuario_logado = st.session_state['agz_lib_user'].usuario_logado
    if (usuario_logado.perfil == 'Admin'):
        opcoes_main['clock-history'] = 'Log'    
    opcoes_main['box-arrow-left'] = 'Sair'

# montar o menu principal (sidebar) e retornar a opção que está selecionada
if 'selected_menu' not in st.session_state:
    st.session_state['selected_menu'] = 0

if 'tour_screen' not in st.session_state or st.session_state['tour_screen'] == 0:
    selecionado = Utilities().montar_menu_main(opcoes_main)
    for x, item in enumerate(opcoes_main):
        if (item == selecionado):
            st.session_state['selected_menu'] = x
        else:
            st.session_state['selected_menu'] = 0

# verifica se existe uma sessão ativa, caso contrario chama função de login
if 'agz_lib_user' not in st.session_state:
    
    with st.spinner('Loading'):
        login = LoginView().verifica_cookie()
    if not login.usuario_logado:
        Credentials.close_db()
        if 'tour_screen' not in st.session_state or st.session_state['tour_screen'] == 0:
            LoginView().incluir_view_login()
            tour_button = st.button('Faça um tour...')
            if tour_button:
                TourScreen()
                st.rerun()
        else:
            TourScreen().incluir_view_tour()
# caso existe um usuário ativo
else:
    if selecionado == 'Dashboard':
        DashView(usuario_logado).incluir_view_dashboard()

    if selecionado == 'Leitura':
        nome_usuario = str(usuario_logado.nome).split(" ")[0]
        st.header(f'Seja bem vindo, {nome_usuario}!')
        LeituraView(usuario_logado).incluir_view_leitura()    

    if selecionado == 'Livros':
        st.header('Gerenciar Livros')
        LivroView(usuario_logado).incluir_view_livro()

    if selecionado == 'Autores':
        st.header('Gerenciar Autores')
        AutorView(usuario_logado).incluir_view_autor()

    if selecionado == 'Editoras':
        st.header('Gerenciar Editoras')
        EditoraView(usuario_logado).incluir_view_editora()

    if selecionado == 'Usuários':
        st.header('Gerenciar Usuários')
        UsuarioView(usuario_logado).incluir_view_usuario()
    
    if selecionado == 'Log':
        st.header('Logs do Sistema')
        LogView().incluir_view_log()

    if selecionado == 'Sair':
        LoginView().fazer_logout()
       

