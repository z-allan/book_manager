import streamlit as st
from models import Login
from streamlit import secrets

class TourScreen:

    _user = None

    def __init__(self):
        st.session_state['tour_screen'] = 1

    def incluir_view_tour(self):
        """
            Monta a tela para iniciar o tour.
            Ao clicar em iniciar:
            * é criado uma sessão de 15 minutos para o usuário;
            * um banco em memória é inicializado e populado.
        """
        st.header('Conheça a nossa aplicação...')
        st.divider()
        st.text('A sessão deste tour ficará disponível por 5 minutos.')
        st.text('Este usuário tem permissão apenas de visualização das funcionalidades.')
        iniciar = st.button(label='Iniciar tour...')
        if iniciar:
            st.session_state['tour_screen'] = 0
            self._user = Login().login_usuario(secrets.tour.user, secrets.tour.password)
            if self._user:
               self._user.autenticar_usuario()          
        st.divider()
        voltar = st.button(label='Voltar')
        if voltar:
           st.session_state['tour_screen'] = 0
           st.rerun()
