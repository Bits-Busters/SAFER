from django.db import models
from SAFERapp.models import CustomUser
from SAFERapp.beans.Enums import RelacaoUFRPE, Registro, Local, StatusChamado
from django.utils.timezone import now

class Ocorrencia(models.Model):
    Autor = models.ForeignKey(CustomUser, on_delete=models.SET_DEFAULT, default=1, related_name="ocorrencias_criadas")
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
    Referencia = models.CharField(max_length=100)
    DataHora = models.DateTimeField(default=now)
    Status = models.CharField(
        max_length=20,
        choices=StatusChamado.choices,
        default=StatusChamado.ABERTO,
        verbose_name="Status do chamado"
    )
    # Nova chave estrangeira
    Resgatista = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="ocorrencias_analizadas",
        verbose_name="Resgatista responsável"
    )
    Localizacao_x = models.IntegerField(default=0, null=False, blank=False)
    Localizacao_y = models.IntegerField(default=0, null=False, blank=False)


    def alterar_status(self, novo_status: StatusChamado):
        self.Status = novo_status
        self.save()

    def alterar_descricao(self, nova_descricao: str):
        self.Descricao = nova_descricao
        self.save()

    def adicionar_Resgatista(self, Resgatista: CustomUser):
        if Resgatista.is_staff:  # Verifica se o usuário é administrador
            self.Resgatista = Resgatista
            self.save()
        else:
            raise ValueError("O Resgatista deve ser um administrador.")

    def __str__(self) -> str:
        return f"Ocorrência de {self.Autor} em {self.DataHora}"
