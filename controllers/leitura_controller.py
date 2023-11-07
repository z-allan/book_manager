from services import DatabaseConnection

class LeituraController:

    _connection = None

    def __init__(self):
        self._connection = DatabaseConnection()

    def selecionar_leituras_db(self, p_usuario):
        """
            Buscar todas as leituras de determinado Usuario, consultando as tabelas leitura e livro, ordenando pelo ano de inicio de leitura (desc) e pela data de inicio da leitura (asc)
        Args:
            p_usuario (Object): recebe o Usuario que será pesquisado

        Returns:
            list: retorna uma lista com o fetchall de todos os registros da consulta
        """
        sql = "SELECT * FROM leitura a INNER JOIN livro b ON a.idLivro=b.id WHERE idUsuario=? ORDER BY CASE WHEN strftime('%Y',a.dataInicio) IS NULL THEN strftime('%Y',date('now')) ELSE strftime('%Y',a.dataInicio) END DESC, CASE WHEN a.dataInicio IS NULL THEN date('now') ELSE a.dataInicio END ASC"
        dados = [(p_usuario.id)]
        resp = self._connection.search(sql, dados)
        return resp

    def selecionar_leitura_id_db(self, p_id):
        """
            Buscar determinada leitura, consultando as tabelas leitura e livro, através do id da Leitura.

        Args:
            p_id (int): id da leitura que será utilizado na pesquisa

        Returns:
            tuple: retorna o primeiro registro com os dados da consulta.
        """
        sql = 'SELECT * FROM leitura a INNER JOIN livro b ON a.idLivro=b.id WHERE a.id=?'
        dados = [(p_id)]
        resp = self._connection.search(sql, dados)
        return resp[0]

    def adicionar_leitura_db(self,p_leitura):
        """
            Inserir novo registro de Leitura na tabela leitura.

        Args:
            p_leitura (Object): recebe a Leitura que será inserida na base de dados.
        
        Returns:
            int: ultimo id inserido 
        """
        sql = 'INSERT INTO leitura (idUsuario,idLivro,dataInsercao,dataInicio,dataFim,formatoLivro,comentLivro) VALUES (?,?,?,?,?,?,?)'
        dados = (p_leitura.usuario, p_leitura.livro.id, p_leitura.data_ins, p_leitura.data_ini, p_leitura.data_fim, p_leitura.formato, p_leitura.coment_livro)
        resp = self._connection.change(sql,dados)
        return resp

    def alterar_leitura_db(self, p_leitura):
        """
            Alterar um registro na tabela leitura através do seu id.

        Args:
            p_leitura (Object): recebe a Leitura que será alterada.
        """
        sql = 'UPDATE leitura SET idLivro=?, dataInicio=?, dataFim=?, formatoLivro=?, comentLivro=? WHERE id=?'
        dados = (p_leitura.livro.id, p_leitura.data_ini, p_leitura.data_fim, p_leitura.formato, p_leitura.coment_livro, p_leitura.id)
        self._connection.change(sql,dados)

    def remover_leitura_db(self, p_leitura):
        """
            Remover um registro da tabela leitura através do id.

        Args:
            p_leitura (Object): recebe a Leitura que será removida.
        """
        sql = 'DELETE FROM leitura WHERE id=?'
        dados = [(p_leitura.id)]
        self._connection.change(sql,dados)
                