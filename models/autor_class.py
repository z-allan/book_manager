import pandas as pd
from controllers import AutorController
from models import Log


class Autor:

    _controller = None

    def __new__(cls, id=0, nome_real='', pseudonimo='', ano_nasc=0, ano_morte=0, local_nasc='', obs_autor=''):
        if cls._controller == None: 
            cls._controller = AutorController()
        instance = super().__new__(cls)
        return instance

    def __init__(self, id=0, nome_real='', pseudonimo='', ano_nasc=0, ano_morte=0, local_nasc='', obs_autor=''):
        self.id = id
        self.nome_real = nome_real.strip()
        self.pseudonimo = pseudonimo.strip()
        self.ano_nasc = ano_nasc
        self.ano_morte = ano_morte
        self.local_nasc = local_nasc
        self.obs_autor = obs_autor
 
    def adicionar_autor(self):
        """
            Método utilizado para chamar a função que irá inserir o autor no banco de dados.

        Returns:
            String: se ocorreu erro ao inserir, será retornado uma mensagem.
        """
        resultado, value = self._controller.adicionar_autor_db(self)
        log_antes = self.dic_autor()
        self.id = value
        log_dps = self.dic_autor()
        if resultado:
            log = Log('autor','insert',log_antes, log_dps)
        else:
            log = Log('autor','insert',log_antes, value)
        log.adicionar_registro_log()
        return resultado, value

    def alterar_autor(self):
        """
            Método utilizado para chamar a função que irá alterar um autor no banco de dados.
        """
        resp = self._controller.selecionar_autor_id_db(self.id)
        dado_atual = Autor(resp[0], resp[1], resp[2], resp[3], resp[4], resp[5], resp[6])
        self._controller.alterar_autor_db(self)
        log_antes = dado_atual.dic_autor()
        log_depois = self.dic_autor()
        log = Log('autor','update',log_antes,log_depois)
        log.adicionar_registro_log()

    def remover_autor(self):
        """
            Método utilizado para chamar a função que irá remover um autor no banco de dados.

        Returns:
            String: se ocorreu erro ao remover, será retornado uma mensagem.
        """
        resp = self._controller.selecionar_autor_id_db(self.id)
        dado_atual = Autor(resp[0], resp[1], resp[2], resp[3], resp[4], resp[5], resp[6])
        resultado = self._controller.remover_autor_db(self)
        log_antes = dado_atual.dic_autor()
        if resultado == None:
            log = Log('autor','delete',log_antes)
        else:
            log = Log('autor','delete',log_antes,resultado)
        log.adicionar_registro_log()
        return resultado

    def __str__(self):
        """
            Método toString do objeto.

        Returns:
            String: retorna o pseudonimo como informação principal do objeto Autor.
        """
        return self.pseudonimo

    def __eq__(self, other):
        """
            Método utilizado para comparar 2 objetos do tipo Autor.

        Args:
            other (Object): objeto que será comparado

        Returns:
            bool: compara o pseudonimo e o id, caso sejam iguais significa que são o mesmo objeto.
        """
        if not isinstance(other, Autor):
            return False
        return self.pseudonimo == other.pseudonimo and self.id == other.id

    def dic_autor(self):
        """
            Método para criar um dicionário com as informações que retornam do banco de dados.

        Returns:
            dict: dicionário com as informações que serão utilizadas para montar o grid.
        """
        return {'Pseudonimo': self.pseudonimo, 'Nome': self.nome_real,  'Ano Nascimento': self.ano_nasc, 'Ano Morte': self.ano_morte, 'Local Nascimento': self.local_nasc, 'Observação': self.obs_autor, 'Id': self.id}

    def montar_df_autor(self):
        """
            Método para criar um dataframe com os registros do banco de dados.
        Returns:
            DataFrame: dataframe com as informações dos autores.
        """
        criar_autor = [Autor(row[0], row[1], row[2], row[3], row[4], row[5], row[6]) for row in self._controller.selecionar_autores_db()]
        df = pd.DataFrame([autor.dic_autor() for autor in criar_autor])
        return df
