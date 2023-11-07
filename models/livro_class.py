from controllers import LivroController, EditoraController, AutorController
from models import Editora, Autor, Log
import pandas as pd

class Livro:

    _controller = None
    _controller_editora = None
    _controller_autor = None

    def __new__(cls, id=0, nome='', edicao=0, num_pag=0, obs_livro='', autor='', editora=None):
        if cls._controller == None:
            cls._controller = LivroController()
        if cls._controller_editora == None:
            cls._controller_editora = EditoraController()
        if cls._controller_autor == None:
            cls._controller_autor = AutorController()
        instance = super().__new__(cls)
        return instance

    def __init__(self, id=0, nome='', edicao=0, num_pag=0, obs_livro='', autor='', editora=None):
        self.id = id 
        self.nome = nome
        self.edicao = edicao
        self.num_pag = num_pag
        self.obs_livro = obs_livro
        self.autor = autor
        self.editora = editora

    def adicionar_livro(self):
        """
            Método utilizado para verificar se determinado livro já existe e em caso negativo, chamar a função que irá inserir o livro no banco de dados.

        Returns:
            String: caso o livro já exista, retorna uma mensagem.
        """
        if not self._controller.existe_livro_db(self):
            log_antes = self.dic_log_livro()
            self.id = self._controller.adicionar_livro_db(self)
            log_dps = self.dic_log_livro()
            for a in self.autor:
                self._controller.adicionar_autorlivro_db(self, a)
                livro_temp = self
                livro_temp.autor = a
                log_antes_al = livro_temp.dic_log_autorlivro()
                log = Log('autor_livro','insert',log_antes_al)
                log.adicionar_registro_log()
            log = Log('livro','insert',log_antes, log_dps)
            log.adicionar_registro_log()
            return None
        else:
            msg = 'Um livro com este nome, editora e edição já existe. Inclusão cancelada'
            log_antes = self.dic_log_livro()
            log = Log('livro','insert',log_antes,msg)
            log.adicionar_registro_log()
            return msg
        

    def alterar_livro(self):
        """
            Método utilizado para chamar a função que irá alterar um livro no banco de dados.
        """
        resp = self._controller.selecionar_livro_id_db(self.id)

        dado_atual = []
        for row in resp:
            dado_atual.append(Livro(row[0], row[1], row[2], row[3], row[4],
                            Autor(row[5], row[6], row[7], row[8], row[9], row[10], row[11]), Editora(row[12], row[13], row[14], row[15])))

        self._controller.alterar_livro_db(self)
        log_antes = dado_atual[0].dic_log_livro()
        log_depois = self.dic_log_livro()
        log = Log('livro','update',log_antes,log_depois)
        log.adicionar_registro_log()
        self._controller.remover_autorlivro_db(self)
        for item in dado_atual:
            log_antes = item.dic_log_autorlivro()
            log = Log('autor_livro','delete from update',log_antes)
            log.adicionar_registro_log()
        for a in self.autor:
            self._controller.adicionar_autorlivro_db(self, a)
            livro_temp = self
            livro_temp.autor = a
            log_antes = livro_temp.dic_log_autorlivro()
            log = Log('autor_livro','insert from update',log_antes)
            log.adicionar_registro_log()
            

    def remover_livro(self):
        """
            Método utilizado para chamar a função que irá remover um livro no banco de dados.

        Returns:
            String: se ocorreu erro ao remover, será retornado uma mensagem.
        """
        resp = self._controller.selecionar_livro_id_db(self.id)

        dado_atual = []
        for row in resp:
            dado_atual.append(Livro(row[0], row[1], row[2], row[3], row[4],
                            Autor(row[5], row[6], row[7], row[8], row[9], row[10], row[11]), Editora(row[12], row[13], row[14], row[15])))

        resultado = self._controller.remover_livro_db(self)
        if resultado == None:
            for x, item in enumerate(dado_atual):
                if x == 0:
                    log_antes = item.dic_log_livro()
                    log = Log('livro','delete',log_antes)
                    log.adicionar_registro_log()
                log_antes = item.dic_log_autorlivro()
                log = Log('autor_livro','delete',log_antes)
                log.adicionar_registro_log()
        else:
            log_antes = dado_atual[0].dic_log_livro()
            log = Log('livro','delete',log_antes,resultado)
            log.adicionar_registro_log()       
        return resultado


    def __str__(self):
        """
            Método toString do objeto.

        Returns:
            String: retorn a concatenção do titulo, autores e editora.
        """
        if ', ' in self.autor:
            msg = f'Título: {self.nome} | Autores: {self.autor} | Editora: {self.editora}'
        else:
            msg = f'Título: {self.nome} | Autor: {self.autor} | Editora: {self.editora}'
        return msg
    
    def __eq__(self, other): 
        """
            Método utilizado para comparar 2 objetos do tipo Livro.

        Args:
            other (Object): objeto que será comparado

        Returns:
            bool: compara o id, caso sejam iguais significa que são o mesmo objeto.
        """
        if not isinstance(other, Livro):
            return False
        return self.id == other.id

    def concatenar_autores(p_lista_autores):
        """
            Método utilizado para transformar uma lista de autores em uma string separada por virgulas.

        Args:
            p_lista_autores (list): recebe a lista dos autores de determinado livro

        Returns:
            String: os pseudonimo dos autores separados por virgula.
        """
        concat = None
        for autor in p_lista_autores:
            if concat != None:
                concat += f', {autor.pseudonimo}'
            else:
                concat = autor.pseudonimo
        return concat

    def selecionar_livros(self):
        """
            Métodos utilizado para buscar os livros no banco de dados.

            * Como um livro pode ter mais de um autor, é necessario concatenar os autores para melhor exibição

        Returns:
            list: lista de objetos do tipo Livro
        """
        resp = self._controller.selecionar_livros_db()

        db_lista_livros = []
        db_lista_autores = []
        id = 0
        for row in resp:
            if id == row[0]:
                db_lista_autores.append(
                    Autor(row[5], row[6], row[7], row[8], row[9], row[10], row[11]))
                db_lista_livros.pop()
            else:
                db_lista_autores = []
                db_lista_autores.append(
                    Autor(row[5], row[6], row[7], row[8], row[9], row[10], row[11]))
            db_lista_livros.append(Livro(row[0], row[1], row[2], row[3], row[4],
                            db_lista_autores, Editora(row[12], row[13], row[14], row[15])))
            id = row[0]

        lista_livros = []
        autores = None
        for l in db_lista_livros:
            if len(l.autor) > 1:
                 autores = Livro.concatenar_autores(l.autor)
            else:
                 autores = l.autor[0].pseudonimo
            livro = Livro(l.id,l.nome,l.edicao,l.num_pag,l.obs_livro,autores,l.editora)
            lista_livros.append(livro)

        return lista_livros

    def busca_editora_combo(self):
        """
            Método para popular o combo box de editoras que podem ser selecionado para um livro.

            * Insere um registro em branco para ser melhor visualizado na tela.

        Returns:
            list: retorna uma lista de objetos da classe Editora.
        """
        criar_editora = [Editora(row[0],row[1],row[2],row[3]) for row in self._controller_editora.selecionar_editoras_db()]
        return [''] + criar_editora

    def busca_autores_multi(self):
        """
            Método para popular o multi select de autores que podem ser selecionado para um livro.

        Returns:
            list: retorna uma lista de objetos da classe Autor.
        """
        criar_autor = [Autor(row[0], row[1], row[2], row[3], row[4], row[5], row[6]) for row in self._controller_autor.selecionar_autores_db()]
        return criar_autor
    
    def busca_autores_selecionado(self,p_lista_selecionado):
        """
            Método para verificar quais autores devem ser populados no multi select quando um registro for selecionado na grid.
        Args:
            p_lista_selecionado (list): recebe uma lista com o pseudonimo dos autores.

        Returns:
            list: uma lista com objetos da classe Autor
        """
        lista_autores = []
        for a in p_lista_selecionado:
            resp = self._controller_autor.selecionar_autor_pseudonimo_db(a)
            lista_autores.append(Autor(resp[0], resp[1], resp[2], resp[3], resp[4], resp[5], resp[6]))
        return lista_autores

    def busca_editora_selecionada(self,p_nome_editora):
        """
            Método para verificar o index de determinada editora que foi selecionada na grid para popular corretamente o combo box.

        Args:
            p_nome_editora (String): recebe o nome da editora que foi selecionada

        Returns:
            int: index da editora
        """
        resp = self._controller_editora.selecionar_editora_nome_db(p_nome_editora)
        return Livro().busca_editora_combo().index(Editora(resp[0],resp[1],resp[2],resp[3]))

    def dic_livro(self):
        """
            Método para criar um dicionário com as informações que retornam do banco de dados.

        Returns:
            dict: dicionário com as informações que serão utilizadas para montar o grid.
        """
        return {'Nome': self.nome, 'Autores': self.autor, 'Editora': self.editora.nome, 'Edicao': self.edicao, 'Nº Paginas': self.num_pag, 'Observação': self.obs_livro, 'Id': self.id}
    

    def montar_df_livro(self):
        """
            Método para criar um dataframe com os registros do banco de dados.
        
        Returns:
            DataFrame: dataframe com as informações dos livros.
        """
        df = pd.DataFrame(
            [livro.dic_livro() for livro in self.selecionar_livros()])
        return df
    
    def dic_log_livro(self):
        """
            Método para criar um dicionário com as informações que retornam do banco de dados.

        Returns:
            dict: dicionário com as informações que serão utilizadas no registro de log
        """
        return {'Nome': self.nome, 'Editora': self.editora.id, 'Edicao': self.edicao, 'Nº Paginas': self.num_pag, 'Observação': self.obs_livro, 'Id': self.id}
    
    def dic_log_autorlivro(self):
        """
            Método para criar um dicionário com as informações que retornam do banco de dados.

        Returns:
            dict: dicionário com as informações que serão utilizadas no registro de log
        """
        return {'Nome Livro': self.nome, 'Id Livro': self.id, 'Nome Autor': self.autor.pseudonimo, 'Id Autor': self.autor.id}