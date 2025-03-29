from django.db import models
from SAFERapp.beans.Ocorrencia import Ocorrencia
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from PIL import Image  # Para verificar se o arquivo é realmente uma imagem

def validator_tamanho_maximo(image):
    if image.file.size > 1024*1024:
        raise ValidationError("Imagem maior que 1MB")

def validator_image_file(image):
    try:
        imagem = Image.open(image)
        imagem.verify()
    except Exception as e:
        raise ValidationError("O arquivo não é uma imagem")
class Imagens(models.Model):
    IdOcorrencia = models.ForeignKey(Ocorrencia, on_delete=models.CASCADE, default=1, related_name="Imagens_registradas")
    Image = models.ImageField(upload_to='imagens/',
                              validators=[validator_tamanho_maximo, # verifica tamanho da imagem
                                          validator_image_file, # verifica se é uma imagem
                                          FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])  # verica se extensão é válida
                                          ],
    )