from abc import ABC, abstractmethod
from ..utils.enums.tipo_dispositivo import TipoDispositivo
from ..utils.enums.estado_dispositivo import EstadoDispositivo
from datetime import datetime

class Dispositivo:
    _next_id = 1  # Contador de clase para IDs únicos

    def __init__(self, nombre: str, tipo: TipoDispositivo, ubicacion: str):
        # Atributos de identificación
        self.id = self.crear_id()
        self.nombre = nombre
        self.tipo = tipo
        self.ubicacion = ubicacion

        # Atributos de estado y configuración
        self._estado = EstadoDispositivo.INACTIVO
        self._fecha_creacion = datetime.now()
        self._fecha_ultima_conexion = None
        self.conectado = False

        # Atributos de operación
        self._bateria = 100  # Porcentaje de batería
        self._intervalo_lectura = 60  # Intervalo de lectura en segundos
        


    @abstractmethod
    def leer_datos(self):
        # Metodo para lectura de datos, debe ser implementado en subclases
        pass

    @abstractmethod
    def procesar_datos(self, datos):
        # Metodo para procesar datos, puede ser sobrescrito en subclases
        pass

    # Metodos Comunes a todos los dispositivos
    @staticmethod
    def crear_id_lista(id_lista: list) -> int:
        # Filtrar sólo enteros positivos
        ids_validos = [x for x in id_lista if isinstance(x, int) and x > 0]
        if not ids_validos:
            nuevo_id = 1
        else:
            nuevo_id = max(ids_validos) + 1
        id_lista.append(nuevo_id)
        return nuevo_id
    
    def activar(self):
        self._estado = EstadoDispositivo.ACTIVO
        self.conectado = True
        self._fecha_ultima_conexion = datetime.now()
        return True
    
    def desactivar(self):
        self._estado = EstadoDispositivo.INACTIVO
        self.conectado = False
        return False
    
    def get_dispositivo(self) -> dict:
        return{
            "id": self.id,
            "nombre": self.nombre,
            "tipo": self.tipo.value,
            "ubicacion": self.ubicacion,
            "estado": self._estado.value,
            "fecha_creacion": self._fecha_creacion.strftime("%Y-%m-%d %H:%M:%S"),
            "fecha_ultima_conexion": self._fecha_ultima_conexion.strftime("%Y-%m-%d %H:%M:%S") if self._fecha_ultima_conexion else None,
            "conectado": self.conectado,
            "bateria": self._bateria,
            "intervalo_lectura": self._intervalo_lectura
        }
    
    def verificar_salud(self) -> bool:
        salud = True
        if self._bateria < 10:
            self._estado = EstadoDispositivo.FALLA
            salud = False
        if not self.conectado:
            self._estado = EstadoDispositivo.INACTIVO
            salud = False
        if self._estado == EstadoDispositivo.MANTENIMIENTO:
            salud = False
        return salud