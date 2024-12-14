from django.db import models
from django.utils.translation import gettext_lazy as _

# Enums no Django
class RelacaoUFRPE(models.TextChoices):
    DOCENTE = 'docente', _('Docente')
    DISCENTE = 'discente', _('Discente')
    TECNICO = 'tecnico', _('Técnico')
    TERCEIRIZADO = 'terceirizado', _('Terceirizado')
    VISITANTE = 'visitante', _('Visitante')


class TipoUsuario(models.TextChoices):
    ADMIN = 'admin', _('Administrador')
    GESTOR = 'gestor', _('Gestor')
    ANALISTA = 'analista', _('Analista')
    COMUM = 'comum', _('Comum')


class Registro(models.TextChoices):
    PRESENCA = 'presenca', _('Presença')
    INTERVENCAO = 'intervencao', _('Intervenção')


class Status(models.TextChoices):
    ABERTO = 'aberto', _('Aberto')
    EM_ANALISE = 'em_analise', _('Em análise')
    FECHADO = 'fechado', _('Fechado')
