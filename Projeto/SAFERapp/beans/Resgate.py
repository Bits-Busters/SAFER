from django.db import models
from SAFERapp.models import CustomUser
import Ocorrencia
from django.utils.timezone import now, datetime

class Resgate(models.Model):
    Ocorrencia = models.ForeignKey(Ocorrencia, on_delete=models.CASCADE, related_name="resgates")
    Resgatista = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="resgates")
    DataHora_Abertura = models.DateTimeField(default=now)
    DataHora_Fechamento = models.DateTimeField(null=True, blank=True)

    # Ocorrencia e Resgatista devem ser únicos juntos, chave primária composta
    class Meta:
        unique_together = ("Ocorrencia", "Resgatista")  # Restrições de unicidade
        
    def adicionar_Resgatista(self, Resgatista: CustomUser):
        if Resgatista.is_staff:  # Verifica se o usuário é administrador
            self.Resgatista = Resgatista
            self.save()
    
    def fechar_resgate(self, data_hora_fechamento: datetime):
        if data_hora_fechamento is not None:
            self.DataHora_Fechamento = data_hora_fechamento
        else:
            self.DataHora_Fechamento = now
        self.save()
        return