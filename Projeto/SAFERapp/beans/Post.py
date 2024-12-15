from django.db import models
from SAFERapp.models import CustomUser

class Post(models.Model):
    Id = models.AutoField(primary_key=True)
    Id_Autor = models.ForeignKey(CustomUser, on_delete= models.CASCADE)
    Titulo = models.CharField(max_length=100)
    Texto = models.TextField()
    Data = models.DateTimeField()

    def alterar_descricao(self, nova_descricao: str):
        return
    
    def excluir_post(self):
        return
    
    def __str__(self):
        return self.Titulo
