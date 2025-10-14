from abc import ABC, abstractmethod
from utils.enums.tipo_dispositivo import TipoDispositivo
from utils.enums.estado_dispositivo import EstadoDispositivo
from datetime import datetime

class Dispositivo:
    _next_id = 1  # Contador de clase para IDs únicos

    def __init__(self, nombre: str, tipo: TipoDispositivo, ubicacion: str):
        # Atributos de identificación
        self._id = self.crear_id()
        self._nombre = nombre
        self._tipo = tipo

        # Atributos de estado y configuración
        self._estado = EstadoDispositivo.INACTIVO
        self._fecha_creacion = datetime.now()
        
    # Getters y setters para todos los atributos
    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, value):
        self._nombre = value

    @property
    def tipo(self):
        return self._tipo

    @tipo.setter
    def tipo(self, value):
        self._tipo = value

    @property
    def estado(self):
        return self._estado

    @estado.setter
    def estado(self, value):
        self._estado = value

    # Metodos Comunes a todos los dispositivos
    def get_dispositivo(self) -> dict:
        return{
            "id": self.id,
            "nombre": self.nombre,
            "tipo": self.tipo.value,
            "estado": self._estado.value,
        }