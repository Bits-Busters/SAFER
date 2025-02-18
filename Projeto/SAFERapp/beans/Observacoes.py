from django.db import models
from SAFERapp.models import CustomUser
from SAFERapp.beans.Ocorrencia import Ocorrencia
from django.utils.timezone import now

class Observacoes(models.Model):
    ocorrencia = models.ForeignKey(Ocorrencia, on_delete=models.CASCADE, related_name="observacoes")
    autor = models.ForeignKey(CustomUser, on_delete=models.SET_DEFAULT, default=1, related_name="observacoes")
    dataHora = models.DateTimeField(default=now)
    corpo = models.TextField()

    def alterar_corpo(self, novo_corpo: str):
        self.Corpo = novo_corpo
        self.save()

    def excluir_observacao(self):
        self.delete()
        return
    
    def __str__(self):
        return self.corpo