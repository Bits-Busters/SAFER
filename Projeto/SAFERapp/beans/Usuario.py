from Enums import RelacaoUFRPE, TipoUsuario, Registro, Status
from Ocorrencia import Ocorrencia

class Usuario():
    def __init__(self, nome: str, email: str, senha: str, telefone: str, telefoneFixo: str, relacaoUFRPE: RelacaoUFRPE, tipoUsuario: TipoUsuario = TipoUsuario.comum):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.telefone = telefone
        self.telefoneFixo = telefoneFixo
        self.relacaoUFRPE = relacaoUFRPE
        self.tipoUsuario = tipoUsuario

    def __str__(self) -> str:
        return f"Usuário: {self.nome}, Tipo: {self.tipoUsuario.name}, Relação: {self.relacaoUFRPE.name}"

    def atualizar_informacoes(self, nome: str = None, email: str = None, telefone: str = None, telefoneFixo: str = None):
        """
        Atualiza as informações pessoais do usuário.
        """
        if nome:
            self.nome = nome
        if email:
            self.email = email
        if telefone:
            self.telefone = telefone
        if telefoneFixo:
            self.telefoneFixo = telefoneFixo
    
    def recuperar_senha(self):
        return
    
    def promover_usuario(self, novo_tipo: TipoUsuario):
        return
    
    def excluir_usuario(self):
        return

    def postar(self, descricao: str):
        return
    
    def alterar_post(self, post, nova_descricao: str):
        return
    
    def excluir_post(self):
        return
    
    def realizar_ocorrencia(self, descricao: str, local, imagens, registro: Registro):
        return
    
    def atualizar_ocorrencia(self, ocorrencia: Ocorrencia, descricao: str, status: Status):
        return
    
    def excluir_ocorrencia(self, ocorrencia: Ocorrencia):
        return