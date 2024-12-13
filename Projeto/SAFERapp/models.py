from django.db import models
from SAFERapp.beans.Enums import RelacaoUFRPE

# Create your models here.

class Usuario(models.Model):
    Id = models.AutoField(primary_key= True,)
    Nome = models.CharField(max_length=100)
    Senha = models.CharField(max_length=100)
    Email = models.CharField(max_length=100)
    RelacaoUFRPE = models.IntegerField(
        choices=[(relacao.value[0], relacao.value[1]) for relacao in RelacaoUFRPE],
        default= RelacaoUFRPE.visitante.value[0]
    )

    def __str__(self):
        return self.Nome
