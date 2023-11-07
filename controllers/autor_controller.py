from services import DatabaseConnection

class AutorController:
    
    _connection = None

    def __init__(self):
        self._connection = DatabaseConnection()

    def selecionar_autores_db(self):
        """
            Buscar todos os autores, com todos os campos da tabela autor ordenando pelo pseudonimo.
        Returns:
            list: retorna o fetchall de todos registros da consulta.
        """
        sql = 'SELECT * FROM autor ORDER BY nomeFantasia'
        resp = self._connection.search(sql)
        return resp


    def selecionar_autor_pseudonimo_db(self, p_nome):
        """
            Buscar um autor específico através do seu pseudonimo, e retornar todos os campos da tabela autor.

        Args:
            p_nome (String): pseudonimo do autor que será utilizado na consulta

        Returns:
            tuple: retorna o primeiro registro com os dados da consulta.
        """
        sql = 'SELECT * FROM autor WHERE nomeFantasia=?'
        dados = [(p_nome)]
        resp = self._connection.search(sql, dados)
        return resp[0]

    def selecionar_autor_id_db(self, p_id):
        """
            Buscar um autor específico através do seu id, e retornar todos os campos da tabela autor.

        Args:
            p_id (int): id do autor que será utilizado na consulta

        Returns:
            tuple: retorna o primeiro registro com os dados da consulta.
        """
        sql = 'SELECT * FROM autor WHERE id=?'
        dados = [(p_id)]
        resp = self._connection.search(sql, dados)
        return resp[0]


    def adicionar_autor_db(self, p_autor):
        """
            Inserir um novo registro de autor na tabela autor.

        Args:
            p_autor (Object): recebe o Autor que será inserido na base

        Returns:
            bool: true se ok e false nok
            String: ultimo id inserido se ok e a mensagem de erro caso nok
        """
        try:
            sql = 'INSERT INTO autor (nomeAutor,nomeFantasia,anoNascimento,anoMorte,localNascimento,obsAutor) VALUES(?,?,?,?,?,?)'
            dados = (p_autor.nome_real, p_autor.pseudonimo, p_autor.ano_nasc,
                    p_autor.ano_morte, p_autor.local_nasc, p_autor.obs_autor)
            resp = self._connection.change(sql,dados)
            return True, resp
        except Exception:
            return False, 'Um autor com este pseudônimo já existe, inclusão cancelada'


    def alterar_autor_db(self, p_autor):
        """
            Alterar um registro na tabela autor através do id do Autor.

        Args:
            p_autor (Object): recebe o Autor que será alterado
        """
        sql = 'UPDATE autor SET nomeAutor=?, nomeFantasia=?, anoNascimento=?, anoMorte=?, localNascimento=?, obsAutor=? WHERE id=?'
        dados = (p_autor.nome_real, p_autor.pseudonimo, p_autor.ano_nasc,
                p_autor.ano_morte, p_autor.local_nasc, p_autor.obs_autor, p_autor.id)
        self._connection.change(sql,dados)


    def remover_autor_db(self, p_autor):
        """
            Remover um registro na tabela autor através do id do Autor.
        Args:
            p_autor (Object): recebe o Autor que será removido.

        Returns:
            String: caso não seja possível remover o registro, retorna uma mensagem.
        """
        try:
            sql = 'DELETE FROM autor WHERE id=?'
            dados = [(p_autor.id)]
            self._connection.change(sql,dados)
            return None
        except Exception:
            return 'Não é possível remover o autor, pois ele está associado a um livro.'
