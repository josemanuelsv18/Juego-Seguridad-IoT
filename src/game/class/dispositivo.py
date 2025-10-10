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
    def ubicacion(self):
        return self._ubicacion

    @ubicacion.setter
    def ubicacion(self, value):
        self._ubicacion = value

    @property
    def estado(self):
        return self._estado

    @estado.setter
    def estado(self, value):
        self._estado = value

    @property
    def fecha_creacion(self):
        return self._fecha_creacion

    @fecha_creacion.setter
    def fecha_creacion(self, value):
        self._fecha_creacion = value

    @property
    def fecha_ultima_conexion(self):
        return self._fecha_ultima_conexion

    @fecha_ultima_conexion.setter
    def fecha_ultima_conexion(self, value):
        self._fecha_ultima_conexion = value

    @property
    def conectado(self):
        return self._conectado

    @conectado.setter
    def conectado(self, value):
        self._conectado = value

    @property
    def bateria(self):
        return self._bateria

    @bateria.setter
    def bateria(self, value):
        self._bateria = value

    @property
    def intervalo_lectura(self):
        return self._intervalo_lectura

    @intervalo_lectura.setter
    def intervalo_lectura(self, value):
        self._intervalo_lectura = value


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

    def _consumir_bateria(self, consumo: int = 1):
        #Simula el consumo de batería del dispositivo
        self._bateria -= consumo
        if self._bateria <= 0:
            self.desactivar()
        return self._bateria
    
    def _notificar_evento(self, evento: str, datos: dict = None):
        # Notifica el evento de un dispositivo
        notificacion = {
            "dispositivo_id": self.id,
            "evento": evento,
            "datos": datos,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        return notificacion