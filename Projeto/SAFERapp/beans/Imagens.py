from django.db import models
from SAFERapp.beans.Ocorrencia import Ocorrencia


class Imagens(models.Model):
    IdOcorrencia = models.ForeignKey(Ocorrencia, on_delete=models.CASCADE, default=1, related_name="Imagens_registradas")
    Image = models.ImageField(upload_to='imagens/')

