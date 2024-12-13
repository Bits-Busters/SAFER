from enum import Enum

class RelacaoUFRPE(Enum):
    docente = 1, "Docente"
    discente = 2, "Discente"
    tecnico = 3, "Técnico"
    terceirizado = 4, "Terceirizado"
    visitante = 5, "Visitante"

class TipoUsuario(Enum):
    admin = 1, "Admin"
    gestor = 2, "Gestor"
    analista = 3, "Analista"
    comum = 4, "Comum"

class Registro(Enum):
    presenca = 1, "Presença"
    intervencao = 2, "Intervenção"

class Status(Enum):
    aberto = 1, "Aberto"
    emAnalise = 2, "Em andamento"
    fechado = 3, "Fechado"