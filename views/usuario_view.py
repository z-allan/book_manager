import streamlit as st
from services.util import Utilities
from models import Usuario

class UsuarioView:

    _util = Utilities()
    _user = None

    def __init__(self, p_usuario=None):
        self._user = p_usuario

 
    def incluir_view_usuario(self):
        """
            Monta a tela para gerenciamento de usuários.
            * Grid com todos os usuários, onde você pode selecionar algum usuário.
            * Incluir: formulário para incluir um novo usuário.
            * Alterar: ao selecionar um usuário na grid, é possível alterar as informações

        Args:
            p_usuario (Object): recebe o usuário que está logado para verificar o perfil
        """

        # monta grid com os usuários
        tour_user = self._user.perfil == 'Tour'
        if self._user.perfil != 'User' and not tour_user:
            df_usuario = Usuario().montar_df_usuario()
            grid_resp = self._util.montar_grid(df_usuario, 'FIT_ALL_COLUMNS_TO_VIEW')
            selecionado = grid_resp['selected_rows']
        else: 
            selecionado = None
        
        # verifica o perfil do usuário
        # usuários do perfil admin podem inserir/alterar usuários
        desabilitado = False
        if self._user.perfil != 'Admin':
            desabilitado = True

        # caso existe algum usuário selecionado na grid, habilita para editar
        if selecionado:
            st.subheader('Alterar Usuário')

            # campos que serão apresentado para o usuário informar
            # caso o usuário não tenha perfil, os campos estarão desabilitados
            with st.form(key='form_alterar_usuario'):
                    st.text_input(key='upd_nome', label='Nome Completo:',max_chars=150, value=selecionado[0]['Nome'], disabled=desabilitado)
                    col1, col2 = st.columns((1, 1))
                    col1.selectbox(key='upd_perfil', label='Perfil do Usuário',options=Usuario.lista_perfis, index=Usuario.lista_perfis.index(selecionado[0]['Perfil']), disabled=desabilitado)
                    radio_options = ['Sim','Não']
                    col2.radio(key='upd_ativo', label='Está ativo?',options=radio_options, horizontal=True,index=radio_options.index(selecionado[0]['Ativo']), disabled=desabilitado)
                    # ao realizar submit ele chama a função alterar_usuario
                    st.form_submit_button('Alterar', on_click=self.alterar_usuario(selecionado[0]['Id']), disabled=desabilitado, type='primary')
            
            # verifica se existe alguma mensagem de retorno ao alterar
            if 'upd_war_msg' in st.session_state:
                st.warning(st.session_state['upd_war_msg'])
                del st.session_state['upd_war_msg']
            if 'upd_err_msg' in st.session_state:
                st.error(st.session_state['upd_err_msg'])
                del st.session_state['upd_err_msg']
            if 'upd_suc_msg' in st.session_state:
                st.toast(st.session_state['upd_suc_msg'], icon="✅")
                st.markdown("""
                <style>
                    div[data-baseweb="toast"]
                    {
                        background-color: #CCFFCC;
                    } 
                </style>
                """,unsafe_allow_html=True) 
                del st.session_state['upd_suc_msg']

        # caso não exista usuário selecionado, exibe o formulários de alterar senha e de inserir usuário
        else:
            # monta menu com opção de alterar usuário e inserir usuário
            tab_selec = self._util.montar_menu_usuario({'gear':'Alterar Senha','person-circle':'Incluir Usuário'})

            # se a aba de alterar senha estiver selecionada
            if tab_selec == 'Alterar Senha':
                st.subheader(f'Alterar senha do usuário: {self._user.nome} ({self._user.login})')
                
                # campos do formulário que serão apresentado para o usuário informar
                with st.form(key='alterar_senha', clear_on_submit=True):
                    st.text_input(key='pass_atual',label='Senha atual:',max_chars=30, type='password', disabled=tour_user)
                    st.text_input(key='pass_novo',label='Nova Senha:',max_chars=30, type='password', disabled=tour_user)
                    st.text_input(key='pass_novo_conf',label='Confirmar Nova senha:',max_chars=30, type='password', value='', disabled=tour_user)
                    # ao realizar submit ele chama a função alterar_senha
                    st.form_submit_button(label='Alterar', on_click=self.alterar_senha(), type='primary', disabled=tour_user)

                # verifica se existe alguma mensagem de retorno ao alterar a senha
                if 'pass_war_msg' in st.session_state:
                    st.warning(st.session_state['pass_war_msg'])
                    del st.session_state['pass_war_msg']
                if 'pass_err_msg' in st.session_state:
                    st.error(st.session_state['pass_err_msg'])
                    del st.session_state['pass_err_msg']
                if 'pass_suc_msg' in st.session_state:
                    st.toast(st.session_state['pass_suc_msg'], icon="✅")
                    st.markdown("""
                    <style>
                        div[data-baseweb="toast"]
                        {
                            background-color: #CCFFCC;
                        } 
                    </style>
                    """,unsafe_allow_html=True) 
                    del st.session_state['pass_suc_msg']

            # se a aba inserir usuário estiver selecionada
            if tab_selec == 'Incluir Usuário':
                st.subheader('Incluir Usuário')

                # campos que serão apresentado para o usuário informar
                # caso o usuário não tenha perfil, os campos estarão desabilitados
                with st.form(key='incluir_usuario'):
                    st.text_input(key='ins_nome', label='Nome Completo:', max_chars=150, value='', disabled=desabilitado)
                    st.text_input(key='ins_usuario', label='Usuario:', max_chars=20, value='', disabled=desabilitado)
                    col1, col2 = st.columns((1, 1))
                    col1.text_input(key='ins_senha', label='Senha:',max_chars=30, type='password', value='', disabled=desabilitado)
                    col1.text_input(key='ins_conf_senha', label='Confirmar Senha:', max_chars=30, type='password', value='', disabled=desabilitado)
                    col2.selectbox(key='ins_perfil', label='Perfil do Usuário',options=Usuario.lista_perfis, index=2, disabled=desabilitado)
                    col2.radio(key='ins_ativo', label='Está ativo?',options=['Sim', 'Não'], horizontal=True, disabled=desabilitado)
                    # ao realizar submit ele chama a função inserir_usuario
                    st.form_submit_button('Adicionar', on_click=self.inserir_usuario, disabled=desabilitado, type='primary')

                # verifica se existe alguma mensagem de retorno ao alterar a senha
                if 'ins_war_msg' in st.session_state:
                    st.warning(st.session_state['ins_war_msg'])
                    del st.session_state['ins_war_msg']
                if 'ins_err_msg' in st.session_state:
                    st.error(st.session_state['ins_err_msg'])
                    del st.session_state['ins_err_msg']
                if 'ins_suc_msg' in st.session_state:
                    st.toast(st.session_state['ins_suc_msg'], icon="✅")
                    st.markdown("""
                    <style>
                        div[data-baseweb="toast"]
                        {
                            background-color: #CCFFCC;
                        } 
                    </style>
                    """,unsafe_allow_html=True) 
                    del st.session_state['ins_suc_msg']


    def cadastrar_usuario(self):
        """
            Função utilizada para validar formulário de cadastrar usuário e inserir o novo usuário 
            * Todo cadastro recebe perfil User
        """

        # verifica se existe um submit de cadastro
        if st.session_state['FormSubmitter:form_novo_usuario-Cadastrar']:
            if st.session_state['novo_nome'] == '' or st.session_state['novo_usuario'] == '' or st.session_state['novo_senha'] == '' or st.session_state['novo_conf_senha'] == '':
                st.session_state['novo_war_msg'] = 'Favor preencher os dados.'
            elif st.session_state['novo_senha'] != st.session_state['novo_conf_senha']:
                st.session_state['novo_senha'] = ''
                st.session_state['novo_conf_senha'] = ''
                st.session_state['novo_war_msg'] = 'Senha e confirmação não estão iguais.'
            elif Usuario().dados_usuario(st.session_state['novo_usuario']) != None:
                st.session_state['novo_usuario'] = ''
                st.session_state['novo_war_msg'] = 'Este usuário já existe.'
            # caso passe todas as validações, insere o novo usuário.
            else:
                novo_usuario = Usuario(0, st.session_state['novo_nome'], st.session_state['novo_usuario'],
                                        st.session_state['novo_senha'], 'User', 1)
                novo_usuario.adicionar_usuario()
                st.session_state['novo_suc_msg'] = 'Usuário cadastrado com sucesso.'
                st.session_state['novo_nome'] = ''
                st.session_state['novo_usuario'] = ''
                st.session_state['novo_senha'] = ''
                st.session_state['novo_conf_senha'] = ''
                del st.session_state['novo_nome']
                del st.session_state['novo_usuario']
                del st.session_state['novo_senha']
                del st.session_state['novo_conf_senha']
            

    def alterar_senha(self):
        """
            Função utilizada para validar formulário de alteração de senha e alterar a senha do usuário

        Args:
            p_usuario (Object): recebe o usuário que está logado 
        """

        # verifica se existe um submit de alteração de senha (necessário para não dar exception)
        if 'FormSubmitter:alterar_senha-Alterar' in st.session_state:
            # verifica se este submit é true
            if st.session_state['FormSubmitter:alterar_senha-Alterar']:
                if st.session_state['pass_atual'] == '' or st.session_state['pass_novo'] == '' or st.session_state['pass_novo_conf'] == '':
                    st.session_state['pass_war_msg'] = 'Favor preencher os dados.'
                elif st.session_state['pass_novo'] != st.session_state['pass_novo_conf']:
                    st.session_state['pass_war_msg'] = 'Senha e confirmação não estão iguais.'
                # caso passe todas as validações, altera a senha do usuário.
                else:
                    alterar_senha = self._user.alterar_senha_usuario(st.session_state['pass_atual'], st.session_state['pass_novo'])
                    if not alterar_senha:
                        st.session_state['pass_war_msg'] = 'Senha atual incorreta.'
                    else:
                        st.session_state['pass_suc_msg'] = 'Senha alterada com sucesso.'
                        del st.session_state['pass_atual']
                        del st.session_state['pass_novo']
                        del st.session_state['pass_novo_conf']


    def inserir_usuario(self):
        """
            Função utilizada para validar formulário de inserir usuário por um Admin
        """

        if st.session_state['ins_nome'] == '' or st.session_state['ins_usuario'] == '' or st.session_state['ins_senha'] == '' or st.session_state['ins_conf_senha'] == '':
            st.session_state['ins_war_msg'] = 'Favor preencher todos os campos.'
        elif st.session_state['ins_senha'] != st.session_state['ins_conf_senha']:
            st.session_state['ins_senha'] = ''
            st.session_state['ins_conf_senha'] = ''
            st.session_state['ins_war_msg'] = 'Senha e confirmação não estão iguais.'
        elif Usuario().dados_usuario(st.session_state['ins_usuario']) != None:
            st.session_state['ins_usuario'] = ''
            st.session_state['ins_war_msg'] = 'Este usuário já existe.'
        # caso passe todas as validações, insere o novo usuário.
        else:
            ins_ativo = 1 if st.session_state['ins_ativo'] == 'Sim' else 0

            novo_usuario = Usuario(0, st.session_state['ins_nome'], st.session_state['ins_usuario'],
                                    st.session_state['ins_senha'], st.session_state['ins_perfil'], ins_ativo)
            novo_usuario.adicionar_usuario()
            st.session_state['ins_suc_msg'] = 'Usuário cadastrado com sucesso.'

            st.session_state['ins_nome'] = ''
            st.session_state['ins_usuario'] = ''
            st.session_state['ins_senha'] = ''
            st.session_state['ins_conf_senha'] = ''
            st.session_state['ins_perfil'] = 'User'
            st.session_state['ins_ativo'] = 'Sim'

            del st.session_state['ins_nome']
            del st.session_state['ins_usuario']
            del st.session_state['ins_senha']
            del st.session_state['ins_conf_senha']
            del st.session_state['ins_perfil']
            del st.session_state['ins_ativo']

    def alterar_usuario(self,p_id):
        """
            Função utilizada para validar formulário de alteração de informações de usuário selecionado
        Args:
            p_id (int): id do usuário que será alterado
        """

        # verifica se existe um submit de alteração de usuário (necessário para não dar exception)
        if 'FormSubmitter:form_alterar_usuario-Alterar' in st.session_state:
            # verifica se este submit é true
            if st.session_state['FormSubmitter:form_alterar_usuario-Alterar']:
                if st.session_state['upd_nome'] == '':
                    st.session_state['upd_war_msg'] = 'Favor preencher os dados.'
                # caso passe todas as validações, altera as informações do usuário.
                else:
                    upd_ativo = 1 if st.session_state['upd_ativo'] == 'Sim' else 0
                    usuario_alterado = Usuario(p_id,st.session_state['upd_nome'],None,None,st.session_state['upd_perfil'],upd_ativo)
                    usuario_alterado.alterar_usuario()                    
                    st.session_state['upd_suc_msg'] = 'Usuário alterado com sucesso.'
                    del st.session_state['upd_nome']
                    del st.session_state['upd_perfil'] 
                    del st.session_state['upd_ativo']
            st.rerun()

