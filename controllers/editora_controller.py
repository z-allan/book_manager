from services import DatabaseConnection

class EditoraController:

    _connection = None

    def __init__(self):
        self._connection = DatabaseConnection()

    def selecionar_editoras_db(self):
        """
            Buscar todas as editoras, com todos os campos da tabela editora ordenando pelo nome.
        Returns:
            list: retorna uma lista com o fetchall de todos os registros da consulta
        """
        sql = 'SELECT * FROM editora ORDER BY nomeEditora'
        resp = self._connection.search(sql)
        return resp
        

    def selecionar_editora_nome_db(self, p_nome):
        """
            Buscar uma editora específica, da tabela editora através do nome.

        Args:
            p_nome (String): nome da editora que será pesquisada

        Returns:
            tuple: retorna o primeiro registro com os dados da consulta.
        """
        sql = 'SELECT * FROM editora WHERE nomeEditora=?'
        dados = [(p_nome)]
        resp = self._connection.search(sql, dados)
        return resp[0]

    def selecionar_editora_id_db(self, p_id):
        """
            Buscar uma editora específica, da tabela editora através do id.

        Args:
            p_id (String): id da editora que será pesquisada

        Returns:
            tuple: retorna o primeiro registro com os dados da consulta.
        """
        sql = 'SELECT * FROM editora WHERE id=?'
        dados = [(p_id)]
        resp = self._connection.search(sql, dados)
        return resp[0]

    def adicionar_editora_db(self, p_editora):
        """
            Inserir um novo registro de Editora na tabela editora.

        Args:
            p_editora (Object): recebe a Editora que será inserida na base.

        Returns:
            bool: true se ok e false nok
            String: ultimo id inserido se ok e a mensagem de erro caso nok
        """
        try:
            sql = 'INSERT INTO editora (nomeEditora, dataCriacao, obsEditora) VALUES (?,?,?)'
            dados = (p_editora.nome, p_editora.data_fund, p_editora.obs_editora)
            resp = self._connection.change(sql,dados)
            return True, resp
        except Exception:
            return False, 'Uma editora com este nome já existe, inclusão cancelada'

    def alterar_editora_db(self, p_editora):
        """
            Alterar o registro de uma Editora na tabela editora.

        Args:
            p_editora (Object): recebe a Editora que será alterada.
        """
        sql = 'UPDATE editora SET nomeEditora=?, dataCriacao=?, obsEditora=? WHERE id=?'
        dados = (p_editora.nome, p_editora.data_fund, p_editora.obs_editora, p_editora.id)
        self._connection.change(sql,dados)


    def remover_editora_db(self, p_editora):
        """
            Remover o registro de uma Editora da tabela editora.
        Args:
            p_editora (Object): recebe a Editora que será removida.

        Returns:
            String: caso ocorra erro ao remover, retorna uma mensagem
        """
        try:
            sql = 'DELETE FROM editora WHERE id=?'
            dados = [(p_editora.id)]
            self._connection.change(sql,dados)
            return None
        except Exception:
            return 'Não é possível remover a Editora, pois ela está associada a um livro.'
    