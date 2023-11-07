from datetime import datetime, timedelta, timezone
import streamlit as st
from models import Log, Usuario
from services import Credentials
import bcrypt
import asyncio

class Login:

    usuario_logado:Usuario = None

    async def verifica_cookie(self):
        tem_cookie = await asyncio.wait_for(Credentials.retornar_cookie(), timeout=5)
        if tem_cookie:
            payload = Credentials.verificar_jwt(tem_cookie)
            self.usuario_logado = Usuario().dados_usuario(payload['user'])
            if self.usuario_logado == None:
                Credentials.remover_cookie()
                self.usuario_logado = None
            else:
                self.autenticar_usuario(p_cookie=True)
        else:
            self.usuario_logado = None
        return self

    def login_usuario(self, p_login, p_senha):
        """
            Método utilizado para fazer o login de um usuário.

        Args:
            p_login (String): recebe o login digitado pelo usuário
            p_senha (String): recebe a senha digitada pelo usuário

        Returns:
            Object: objeto da classe Usuario, caso a senha esteja correta.
        """
        log_antes = f"Usuario:'{p_login}' | Tentativa de login"
        log_dps = ''
        temp_user = Usuario()
        self.usuario_logado = temp_user.dados_usuario(p_login)
        if self.usuario_logado:
            if not bcrypt.checkpw(p_senha.encode(),self.usuario_logado.senha.encode()):
                self.usuario_logado = None
                log_dps = f"Usuario:'{p_login}' | Não foi possível realizar o login"
            else:
                log_dps = f"Usuario:'{p_login}' | Login efetuado com sucesso"  
        log = Log('','login',log_antes,log_dps)
        log.adicionar_registro_log()
        return self
    
    def logout_usuario(self):
        """
            Método utilizado para realizar logout do usuário e remover sessão
        """
        log_antes = f"Usuario:'{self.usuario_logado.login}' | Logout do usuário"
        st.session_state['agz_lib_user'] = None
        del st.session_state['agz_lib_user']
        if 'agzlog_opcao' in st.session_state:
            del st.session_state['agzlog_opcao']
            del st.session_state['agzlog_ini']
            del st.session_state['agzlog_fim']
        log_dps = f"Usuario:'{self.usuario_logado.login}' | Sessão e cookie do usuário removidos com sucesso"  
        log = Log('','logout',log_antes,log_dps)
        log.adicionar_registro_log()
    
    def autenticar_usuario(self, p_manter=False, p_cookie=False, p_tour=False):
        """
            Método utilizado para popular uma session com o objeto do tipo Usuario que foi feito o login.

        Args:
            p_manter (bool, optional): select box de manter login, caso seja True, será criado um cookie para 5 dias usuário. Defaults to False.
        """
        self.usuario_logado.senha = None
        st.session_state['agz_lib_user'] = self
        if p_cookie:
            log_antes = f"Usuario:'{self.usuario_logado.login}' | Autenticação do usuário por cookie"
            log_dps = f"Usuario:'{self.usuario_logado.login}' | Autenticação por cookie realizada com sucesso"  
            st.rerun()
        else:
            log_antes = f"Usuario:'{self.usuario_logado.login}' | Autenticação do usuário por login"
            log_dps = f"Usuario:'{self.usuario_logado.login}' | Autenticação por login realizada com sucesso (Manter={p_manter})"  
            if p_tour:
                log_antes = f"Usuario:'{self.usuario_logado.login}' | Autenticação para tour"
                log_dps = ''
                exp_cookie = datetime.now() + timedelta(minutes=5)
                exp_jwt = datetime.now(tz=timezone.utc) + timedelta(minutes=5)
            elif p_manter:
                exp_cookie = datetime.now() + timedelta(days=7)
                exp_jwt = datetime.now(tz=timezone.utc) + timedelta(days=7)
            else:
                exp_cookie = datetime.now() + timedelta(hours=8)
                exp_jwt = datetime.now(tz=timezone.utc) + timedelta(hours=8)
            payload = { 'user': self.usuario_logado.login, 'exp': exp_jwt }
            token = Credentials.criar_jwt(payload)
            Credentials.criar_cookie(token, exp_cookie)
            print(f'criou token {payload}')
            print(f'criou cookie {token}')
        log = Log('','auth',log_antes,log_dps)
        log.adicionar_registro_log()