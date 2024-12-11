from enum import Enum

class RelacaoUFRPE(Enum):
    docente = 1
    discente = 2
    tecnico = 3
    terceirizado = 4
    visitante = 5

class TipoUsuario(Enum):
    admin = 1
    gestor = 2
    analista = 2
    comum = 3

class Registro(Enum):
    presenca = 1
    intervencao = 2

class Status(Enum):
    aberto = 1
    emAnalise = 2
    fechado = 3