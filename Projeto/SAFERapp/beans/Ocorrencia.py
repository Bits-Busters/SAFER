from django.db import models
from SAFERapp.models import CustomUser
from SAFERapp.beans.Enums import Status

class Ocorrencia(models.Model):
    Autor = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    Descricao = models.TextField()
    Local = models.CharField(max_length=100)
    DataHora = models.DateTimeField()
    Status = models.CharField(
        max_length=20,
        choices= Status.choices,
        default = Status.ABERTO,
        verbose_name= "Status do chamado"
    )
    
    def alterar_status(self, novo_status: Status):
        return
    
    def alterar_descricao(self, nova_descricao: str):
        return
    
    def adicionar_analista(self, analista: CustomUser):
        return
    
    def __str__(self) -> str:
        return f"Ocorrência de {self.Autor} em {self.DataHora}"
    
