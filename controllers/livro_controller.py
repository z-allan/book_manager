from services import DatabaseConnection

class LivroController:

    _connection = None

    def __init__(self):
        self._connection = DatabaseConnection()

    def selecionar_livros_db(self):
        """
            Buscar todos os livros, consultando as tabelas livro, autor_livro e autor.

            * Caso um livro tenha mais de um autor, a consulta irá trazer vários registros para aquele livro, então durante a montagem da lista, é feita a verificação para que exista apenas um registro do tipo livro e os autores fiquem em uma lista separada dentro do objeto Livro.

        Returns:
            list: retorna uma lista com o fetchall de todos os registros da consulta
        """
        sql = 'SELECT l.id,l.nomeLivro,l.numEdicao,l.numPaginas,l.obsLivro, a.*, e.* FROM livro l INNER JOIN autor_livro al ON l.id=al.idLivro INNER JOIN autor a ON a.id=al.idAutor INNER JOIN editora e ON l.idEditora=e.id ORDER BY l.nomeLivro, l.id'
        resp = self._connection.search(sql)
        return resp

    def selecionar_livro_id_db(self,p_id):
        """
            Busca um livro pelo id

            * Caso um livro tenha mais de um autor, a consulta irá trazer vários registros para aquele livro, então durante a montagem da lista, é feita a verificação para que exista apenas um registro do tipo livro e os autores fiquem em uma lista separada dentro do objeto Livro.

        Returns:
            list: retorna uma lista com o fetchall de todos os registros da consulta
        """
        sql = 'SELECT l.id,l.nomeLivro,l.numEdicao,l.numPaginas,l.obsLivro, a.*, e.* FROM livro l INNER JOIN autor_livro al ON l.id=al.idLivro INNER JOIN autor a ON a.id=al.idAutor INNER JOIN editora e ON l.idEditora=e.id WHERE l.id=? ORDER BY l.nomeLivro, l.id'
        dados = [(p_id)]
        resp = self._connection.search(sql,dados)
        return resp

    def existe_livro_db(self, p_livro):
        """
            Verificar se determinado livro já existe na tabela, através dos campos: nome, editora e edição.

            * Como os campos não podem ser configurados como UNIQUE na base, é necessário realizar está verificação antes de inserir um novo registro na tabela livro.

        Args:
            p_livro (Object): recebe o Livro que será verificado

        Returns:
            bool: retorna True se o livro já existe e False caso não exista
        """
        sql = 'SELECT * FROM livro WHERE nomeLivro=? and idEditora=? and numEdicao=?'
        dados = (p_livro.nome, p_livro.editora.id, p_livro.edicao)
        resp = self._connection.search(sql, dados)
        rows = len(resp)
        if rows > 0:
            return True
        else:
            return False


    def adicionar_livro_db(self,p_livro):
        """
            Inserir registro na tabela livro.

        Args:
            p_livro (Object): recebe o Livro que será inserido.

        Returns:
            int: ultimo id inserido que será utilizado para inserir os dados na tabela autor_livro
        """
        sql = 'INSERT INTO livro (nomeLivro,idEditora,numEdicao,numPaginas,obsLivro) VALUES (?,?,?,?,?)'
        dados = (p_livro.nome, p_livro.editora.id,
                p_livro.edicao, p_livro.num_pag, p_livro.obs_livro)
        resp = self._connection.change(sql, dados)
        return resp


    def alterar_livro_db(self, p_livro):
        """
            Alterar registro na tabela livro através do id

        Args:
            p_livro (Object): recebe o Livro que sera alterado.
        """
        sql = 'UPDATE livro SET nomeLivro=?, idEditora=?, numEdicao=?, numPaginas=?, obsLivro=? WHERE id=?'
        dados = (p_livro.nome, p_livro.editora.id, p_livro.edicao,
                p_livro.num_pag, p_livro.obs_livro, p_livro.id)
        self._connection.change(sql, dados)


    def remover_livro_db(self, p_livro):
        """
            Remover registro da tabela livro através do id

        Args:
            p_livro (Object): recebe o Livro que sera removido.
        """
        try:
            sql = 'DELETE FROM livro WHERE id=?'
            dados = [(p_livro.id)]
            self._connection.change(sql, dados)
            return None
        except Exception:
            return 'Não é possível remover o livro, pois ela está associada a uma leitura.'


    def remover_autorlivro_db(self, p_livro):
        """
            Remover registro da tabela autor_livro através do id do livro

            * Ao realizar alteração de um livro, os registros de autor são removidos e inseridos novamente nesta tabela.

        Args:
            p_livro (Object): recebe o Livro que será utilizado como parâmetro
        """
        sql = 'DELETE FROM autor_livro WHERE idLivro=?'
        dados = [(p_livro.id)]
        self._connection.change(sql, dados)

    def adicionar_autorlivro_db(self, p_livro, p_autor):
        """
            Inserir registro na tabela autor_livro.

            * Está tabela armazena apenas o id do livro e o id de seus autores.

        Args:
            p_livro (Object): recebe o Livro que será inserido.
            p_autor (Object): recebe os Autores que serão inseridos.
        """
        sql = 'INSERT INTO autor_livro (idLivro,idAutor) VALUES (?, ?)'
        dados = (p_livro.id, p_autor.id)
        self._connection.change(sql, dados)
