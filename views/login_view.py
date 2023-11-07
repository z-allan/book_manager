import asyncio
import streamlit as st
from services import Utilities, Credentials, DatabaseConnection
from models import Login

class LoginView:

    _util = Utilities()
    _user = None

    def verifica_cookie(self):
        """
            Função utilizada para verificar se um usuário já está autenticado (tem cookie) ou se será realizado login/cadastro de um usuário        
        """
        return asyncio.run(Login().verifica_cookie())

    def fazer_logout(self):
        st.session_state['agz_lib_user'].logout_usuario()
        Credentials.remover_cookie()
        DatabaseConnection(close=True)

    def incluir_view_login(self):
        """
            Formulário para realizar login de um usuário
        """
        
        # CSS para alinhar conteúdo a direita da tela
        st.markdown("""
            <style>
                div[data-testid="column"]:nth-of-type(2)  label
                {
                    justify-content: flex-end
                } 
            </style>
        """,unsafe_allow_html=True)   

        # campos que serão apresentado para o usuário informar
        with st.form(key='login_usuario', clear_on_submit=True):
                login_usuario = st.text_input(key='login_usuario', label='Login:')
                login_senha = st.text_input(key='login_senha',
                    label='Senha:', type='password')
                col1, col2 = st.columns(2)
                botao_entrar = col1.form_submit_button('Entrar', type='primary')
                # opção de criar um cookie para manter a sessão do usuário ativa
                login_manter = col2.checkbox(
                    label='Manter conectado', help='Ao selecionar esta opção, você está aceitando manter cookies da sua sessão por 7 dias.', key='login_manter',)

        # ação que será executada ao dar submit no formulário
        if botao_entrar:
            if login_usuario.strip() == '' or login_senha.strip() == '':
                st.warning('Favor preencher os dados')
                st.stop()
            else:
                self._user = Login().login_usuario(login_usuario, login_senha)
                if self._user:
                    self._user.autenticar_usuario(p_manter=login_manter)
                else:
                    st.warning('Login/Senha incorretos')
                    st.stop()

