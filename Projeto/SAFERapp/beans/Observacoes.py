from django.db import models
from SAFERapp.models import CustomUser
import Ocorrencia
from django.utils.timezone import now

class Observacoes(models.Model):
    Ocorrencia = models.ForeignKey(Ocorrencia, on_delete=models.CASCADE, related_name="observacoes")
    Autor = models.ForeignKey(CustomUser, on_delete=models.SET_DEFAULT, default=1, related_name="observacoes")
    DataHora = models.DateTimeField(auto_now_add=now)
    Corpo = models.TextField()

    def alterar_corpo(self, novo_corpo: str):
        self.Corpo = novo_corpo
        self.save()

    def excluir_observacao(self):
        self.delete()
        return