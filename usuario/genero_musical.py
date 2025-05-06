from usuario import Usuario

class GeneroMusical:
    def init(self, nome:str):
        self.nome = nome

    def adicionarGeneroMusical(usuario : Usuario, genero: str):
        usuario.interesses_musicais.append(genero)

    def removerGeneroMusical(usuario : Usuario, genero: str):
        usuario.interesses_musicais.remove(genero)

    #TODO no cadastro, exigir 3 generos musicais
