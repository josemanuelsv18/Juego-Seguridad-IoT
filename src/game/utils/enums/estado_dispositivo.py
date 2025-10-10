from enum import Enum

class EstadoDispositivo(Enum):
    ACTIVO = "Activo"
    INACTIVO = "Inactivo"
    MANTENIMIENTO = "Mantenimiento"
    FALLA = "Falla"