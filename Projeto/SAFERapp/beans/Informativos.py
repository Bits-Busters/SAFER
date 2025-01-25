from django.db import models
from django.utils import timezone
from SAFERapp.models import CustomUser, get_or_create_anonymous_user
from django.core.exceptions import ObjectDoesNotExist


class Informativo(models.Model):
    id = models.AutoField(primary_key=True)
    # Usando o ID do usuário como valor padrão
    id_Autor = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_DEFAULT,
        default= get_or_create_anonymous_user,  # Função que retorna a instância do usuário
        verbose_name="Autor do Informativo"
    )
    titulo = models.CharField(max_length=100, verbose_name="Título do Informativo")
    corpo = models.TextField(verbose_name="Corpo do Informativo")
    imagens = models.ImageField(upload_to='imagens/', verbose_name="Imagens do Informativo")
    data_criacao = models.DateTimeField(default=timezone.now, verbose_name="Data de Criação")


    def alterar_descricao(self, nova_descricao: str):
        self.corpo = nova_descricao
        self.save()
        return
    
    def excluir_informativo(self):
        self.delete()   
        return
