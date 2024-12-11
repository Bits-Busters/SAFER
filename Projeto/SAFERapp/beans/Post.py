from datetime import datetime
from Usuario import Usuario

class Post():
    def __init__(self, usuario: Usuario, descricao: str):
        self.usuario = usuario
        self.descricao = descricao
        self.dataHora = datetime.now()

    def alterar_descricao(self, nova_descricao: str):
        return
    
    def excluir_post(self):
        return
    
    def __str__(self) -> str:
        return f"Post de {self.usuario.nome} em {self.dataHora}"
