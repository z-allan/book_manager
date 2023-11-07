from services import DatabaseConnection


class DashController:

    _connection = None

    def __init__(self):
        self._connection = DatabaseConnection()

    def selecionar_usuario_dash_db(self, p_usuario):
        """
            Buscar dados das tabelas leitura, livro, autor_livro, autor e editora referente a determinado Usuário.

        Args:
            p_usuario (Object): recebe o Usuário que será utilizado na pesquisa

        Returns:
            list: retorna uma lista com o fetchall de todos os registros da consulta
        """
        sql = 'SELECT a.id as idLeitura, a.dataInsercao, a.dataInicio, a.dataFim, a.formatoLivro, a.comentLivro,b.id as idLivro, b.nomeLivro, b.numEdicao, b.numPaginas, b.obsLivro, d.id as idAutor, d.nomeAutor, d.nomeFantasia, d.anoNascimento, d.anoMorte, d.localNascimento, d.obsAutor, e.id as idEditora, e.nomeEditora, e.dataCriacao, e.obsEditora FROM leitura a INNER JOIN livro b ON (a.idLivro=b.id) INNER JOIN autor_livro c ON (b.id=c.idLivro) INNER JOIN autor d ON (c.idAutor=d.id) INNER JOIN editora e ON (b.idEditora=e.id) WHERE a.idUsuario=?'
        dados = [(p_usuario.id)]
        resp = self._connection.search(sql, dados)
        return resp

    def selecionar_total_dash_db(self):
        """
            Buscar dados das tabelas leitura, livro, autor_livro, autor e editora referente a todos usuários.

        Returns:
            list: retorna uma lista com o fetchall de todos os registros da consulta
        """
        sql = 'SELECT a.id as idLeitura, a.dataInsercao, a.dataInicio, a.dataFim, a.formatoLivro, a.comentLivro,b.id as idLivro, b.nomeLivro, b.numEdicao, b.numPaginas, b.obsLivro, d.id as idAutor, d.nomeAutor, d.nomeFantasia, d.anoNascimento, d.anoMorte, d.localNascimento, d.obsAutor, e.id as idEditora, e.nomeEditora, e.dataCriacao, e.obsEditora, a.idUsuario FROM leitura a INNER JOIN livro b ON (a.idLivro=b.id) INNER JOIN autor_livro c ON (b.id=c.idLivro) INNER JOIN autor d ON (c.idAutor=d.id) INNER JOIN editora e ON (b.idEditora=e.id)'
        resp = self._connection.search(sql)
        return resp
