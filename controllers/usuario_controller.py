from services import DatabaseConnection

class UsuarioController:

    _connection = None

    def __init__(self):
        self._connection = DatabaseConnection()

    def dados_usuario_db(self, p_login):
        """
            Buscar um usuário ativo específico através de seu login e retornar todos os campos da tabela usuario.

        Args:
            p_login (String): recebe o login do Usuario que sera consultado.

        Returns:
            tuple: retorna o primeiro registro com os dados da consulta.
        """
        sql = 'SELECT * FROM usuario WHERE loginUsuario=? and usuarioAtivo=1'
        dados=[(p_login)]
        resp = self._connection.search(sql, dados)
        return resp[0] if len(resp) > 0 else None

    def selecionar_usuario_id_db(self, p_id):
        """
            Buscar um usuário ativo específico através de seu login e retornar todos os campos da tabela usuario.

        Args:
            p_login (String): recebe o login do Usuario que sera consultado.

        Returns:
            tuple: retorna o primeiro registro com os dados da consulta.
        """
        sql = 'SELECT * FROM usuario WHERE id=?'
        dados=[(p_id)]
        resp = self._connection.search(sql, dados)
        return resp[0]

    def selecionar_usuarios_db(self):
        """
            Buscar todos os usuarios, retornando todos os campos menos a senha da tabela usuario.
        
        Returns:
            list: retorna uma lista com o fetchall de todos os registros da consulta
        """
        sql = 'SELECT id, nomeUsuario, loginUsuario,perfilUsuario, usuarioAtivo FROM usuario'
        resp = self._connection.search(sql)
        return resp

    def alterar_senha_usuario_db(self, p_usuario, p_nova_senha):
        """
            Alterar senha de determinado Usuario na tabela usuario.

            * As senhas já estão criptografadas.

        Args:
            p_usuario (Object): recebe o Usuario que será alterado.
            p_nova_senha (String): recebe a nova senha que será inserida.
        """
        sql='UPDATE usuario SET senhaUsuario=? WHERE loginUsuario=? and senhaUsuario=?'
        dados=(p_nova_senha, p_usuario.login, p_usuario.senha)
        self._connection.change(sql,dados)

    def adicionar_novo_usuario_db(self, p_usuario):
        """
            Inserir registro na tabela usuario.

            * A senha já está criptografada.

        Args:
            p_usuario (Object): recebe o Usuario que será inserido.
        """
        sql='INSERT INTO usuario VALUES (null,?, ?, ?, ?, ?)'
        dados=(p_usuario.nome, p_usuario.login, p_usuario.senha, p_usuario.perfil, p_usuario.ativo)
        resp = self._connection.change(sql,dados)
        return resp

    def alterar_usuario_db(self,p_usuario):
        """
            Alterar registro na tabela usuario.

            * As informacões que podem ser alteradas são: nome, perfil e se o usuario está ativo.
            * Usuários não são removidos, apenas configurados como inativo.

        Args:
            p_usuario (Object): recebe o Usuario que será alterado
        """
        sql='UPDATE usuario SET nomeUsuario=?, perfilUsuario=?, usuarioAtivo=? WHERE id=?'
        dados=(p_usuario.nome, p_usuario.perfil, p_usuario.ativo, p_usuario.id)
        self._connection.change(sql,dados)
