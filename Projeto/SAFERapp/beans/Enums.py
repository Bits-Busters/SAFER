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
    PRESENCA = 'presenca', _('Presença de animal')
    INTERVENCAO = 'intervencao', _('Intervenção necessária')

class Local(models.TextChoices):
    RU = 'ru', _('RU')
    TRANSRURAL = 'trasrural', _('Transrural')
    BIBLIOTECACENTRAL = 'biblioteca_central', _('Biblioteca Central')
    BIBLIOTECASETORIAL = 'biblioteca_setorial', _('Biblioteca Setorial')
    CEAGRI = 'ceagri', _('CEAGRI')
    CEGOE = 'cegoe', _('CEGOE')
    DEPMED = 'dep_medicina_vet', _('Departamento de Medicina Veterinária')
    DEPZOO = 'dep_zootecnia', _('Departamento de Zootecnia')
    CENTRAL = 'pred_central', _('Prédio Central')
    PREF = 'oref_rural', _('Prefeitura da UFRPE')

class StatusChamado(models.TextChoices):
    ABERTO = 'aberto', _('Aberto')
    EM_ANALISE = 'em_analise', _('Em análise')
    EM_ANDAMENTO = 'em_andamento', _('Em andamento')
    FECHADO = 'fechado', _('Fechado')