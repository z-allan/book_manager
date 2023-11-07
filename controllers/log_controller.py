from services import DatabaseConnection

class LogController:

    _connection = None

    def __init__(self):
        self._connection = DatabaseConnection()

    def adicionar_registro_log_db(self,p_log):
        """
            Inserir um novo registro de Log na tabela log.

        Args:
            p_log (Object): recebe um objeto da classe Log que será inserida na base.
        """
        sql = 'INSERT INTO log VALUES (null,?,?,?,?,?,?)'
        dados = (p_log.timestamp, p_log.usuario, p_log.tabela, p_log.acao, p_log.dado_antes, p_log.dado_depois)
        self._connection.change(sql, dados)

    def selecionar_log_db(self,p_data_ini, p_data_fim):
        """
            Retorna os logs baseado em um range de datas

        Args:
            p_data_ini (datetime): data inicial da pesquisa
            p_data_fim (datetime): data final da pesquisa

        Returns:
            list: retorna uma lista com o fetchall de todos os registros da consulta
        """
        sql = 'SELECT * FROM log WHERE date(timestamp) >= ? and date(timestamp) <= ? ORDER BY id DESC'
        dados = (p_data_ini, p_data_fim)
        resp = self._connection.search(sql, dados)
        return resp