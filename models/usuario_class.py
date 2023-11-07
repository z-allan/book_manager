import bcrypt
import pandas as pd
from models import Log
from controllers import UsuarioController

class Usuario:

    _controller = None

    # perfis possíveis de usuário
    lista_perfis = ['Admin', 'SuperUser','User','Tour']

    def __new__(cls, id=0, nome='', login='', senha='', perfil='User', ativo=0):
        if cls._controller == None:
            cls._controller = UsuarioController()
        instance = super().__new__(cls)
        return instance


    def __init__(self, id=0, nome='', login='', senha='', perfil='User', ativo=0):
        self.id = id
        self.nome = nome        
        self.login = login
        self.senha = senha
        self.perfil = perfil
        self.ativo = ativo 

    def dados_usuario(self,p_login):
        """
            Método para buscar dados de determinado usuário no banco de dados.

        Args:
            p_login (String): recebe o login do usuário que está logado.

        Returns:
            Object: um objeto do tipo Usuario.
        """
        user = self._controller.dados_usuario_db(p_login)
        return Usuario(user[0],user[1],user[2],user[3],user[4],user[5]) if user != None else None
        
    def alterar_senha_usuario(self, p_senha, p_nova_senha):
        """
            Método utilizado para alterar senha do usuário no banco de dados.

            * A senha é criptografada antes se ser enviada para o banco de dados.

        Args:
            p_senha (String): senha atual
            p_nova_senha (String): nova senha

        Returns:
            bool: caso a senha digitada como atual seja a senha que está na base, ele realiza a alteração e retorna True, caso negativo ele retorna False.
        """
        log_antes = f"Usuario:'{self.login}' | Tentativa de alterar senha"
        usuario = self.dados_usuario(self.login)
        if bcrypt.checkpw(p_senha.encode(),usuario.senha.encode()):
            senha_cript = bcrypt.hashpw(p_nova_senha.encode(), bcrypt.gensalt()).decode()
            self._controller.alterar_senha_usuario_db(usuario, senha_cript)
            log_dps = f"Usuario:'{self.login}' | Senha alterada com sucesso"
            resultado = True
        else:
            log_dps = f"Usuario:'{self.login}' | Não foi possível alterar a senha"
            resultado = False
        log = Log('usuario', 'update', log_antes, log_dps)
        log.adicionar_registro_log()
        return resultado
    
    def adicionar_usuario(self):
        """
            Método para chamar a função que irá inserir o usuário no banco de dados.

            * A senha é criptografa nesse momento
        """
        log_antes = self.dic_usuario()
        self.senha = bcrypt.hashpw(self.senha.encode(), bcrypt.gensalt()).decode()
        self.id = self._controller.adicionar_novo_usuario_db(self)
        log_dps = self.dic_usuario()
        log = Log('usuario','insert',log_antes,log_dps)
        log.adicionar_registro_log()

    def alterar_usuario(self):
        """
            Método para chamar a função que irá alterar o usuário no banco de dados.
        """
        user = self._controller.selecionar_usuario_id_db(self.id)
        dado_atual = Usuario(user[0],user[1],user[2],user[3],user[4],user[5])
        self._controller.alterar_usuario_db(self)
        log_antes = dado_atual.dic_usuario()
        log_dps = self.dic_usuario()
        log = Log('usuario','update',log_antes,log_dps)
        log.adicionar_registro_log()

    def dic_usuario(self):
        """
            Método para criar um dicionário com as informações que retornam do banco de dados.

        Returns:
            dict: dicionário com as informações que serão utilizadas para montar o grid.
        """
        self.ativo = 'Sim' if self.ativo == 1 else 'Não'
        return {'Usuario': self.login, 'Nome': self.nome,  'Perfil': self.perfil, 'Ativo': self.ativo, 'Id': self.id}

    def montar_df_usuario(self,):
        """
            Método para criar um dataframe com os registros do banco de dados.
        
        Returns:
            DataFrame: dataframe com as informações dos usuários.
        """
        resp = self._controller.selecionar_usuarios_db()
        criar_usuario = [Usuario(row[0], row[1], row[2], None,row[3], row[4]) for row in resp]
        df = pd.DataFrame(
            [usuario.dic_usuario() for usuario in criar_usuario])
        return df
    
    