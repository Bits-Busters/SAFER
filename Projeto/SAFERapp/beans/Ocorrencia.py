from datetime import datetime
from Enums import Status, Registro, RelacaoUFRPE, TipoUsuario
from Usuario import Usuario

class Ocorrencia():
    def __init__(self, usuario: Usuario, descricao: str, local, imagens, registro: Registro, status: Status = Status.aberto, analista: Usuario = None):
        self.usuario = usuario
        self.descricao = descricao
        self.local = local
        self.imagens = imagens
        self.dataHora = datetime.now()
        self.registro = registro
        self.status = status
    
    def alterar_status(self, novo_status: Status):
        return
    
    def alterar_descricao(self, nova_descricao: str):
        return
    
    def adicionar_analista(self, analista: Usuario):
        return
    
    def __str__(self) -> str:
        return f"Ocorrência de {self.usuario.nome} em {self.dataHora}"
    
