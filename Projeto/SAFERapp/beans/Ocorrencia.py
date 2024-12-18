from django.db import models
from SAFERapp.models import CustomUser
from SAFERapp.beans.Enums import Status, RelacaoUFRPE, Registro
from datetime import datetime
from django.utils.timezone import now

class Ocorrencia(models.Model):
    Autor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=1)
    Nome_Autor = models.CharField(max_length=100)
    Celular_Autor = models.CharField(max_length=20)
    Telefone_Autor = models.CharField(max_length=20)
    Relacao_Autor = models.CharField(
        max_length=20,
        choices=RelacaoUFRPE.choices,
        default=RelacaoUFRPE.VISITANTE,
        verbose_name="Relação com a UFRPE"
    )
    Tipo_Caso = models.CharField(
        max_length=20,
        choices=Registro.choices,
        default=Registro.PRESENCA,
        verbose_name="Tipo do caso"
    )
    Descricao = models.TextField()
    Nome_Animal = models.CharField(max_length=100)
    Local = models.CharField(max_length=100)
    Referencia = models.CharField(max_length=100)
    DataHora = models.DateTimeField(default=now())
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
    
