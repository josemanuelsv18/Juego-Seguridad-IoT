from utils.enums.tipo_dispositivo import TipoDispositivo
import random
from datetime import datetime 
from classes.dispositivo import Dispositivo
 
 
class SensorMovimiento(Dispositivo):
    def __init__(self, nombre: str, ubicación: str, radio_cobertura: float = 10.0):

        super().__init__(nombre, TipoDispositivo.SENSOR_MOVIMIENTO, ubicación)

        #atributos especificos del sensor de movimiento
        self._radio_cobertura = radio_cobertura  # metros
        self._distancia_deteccion_x = None  # metros
        self._distancia_deteccion_y = None  # metros
        self._movimiento_detectado = False
        self._ultimo_movimiento = None
        self._contador_movimientos = 0

    #getters y setters
    @property
    def radio_cobertura(self):
        return self._radio_cobertura
    @radio_cobertura.setter
    def radio_cobertura(self, value):
        self._radio_cobertura = value

    @property
    def ultimo_movimiento(self):
        return self._ultimo_movimiento
    @ultimo_movimiento.setter
    def ultimo_movimiento(self, value):
        self._ultimo_movimiento = value

    @property
    def contador_movimientos(self):
        return self._contador_movimientos
    @contador_movimientos.setter
    def contador_movimientos(self, value):
        self._contador_movimientos = value

    @property
    def distancia_deteccion_x(self):
        return self._distancia_deteccion_x
    @distancia_deteccion_x.setter
    def distancia_deteccion_x(self, value):
        self._distancia_deteccion_x = value

    @property
    def distancia_deteccion_y(self):
        return self._distancia_deteccion_y
    @distancia_deteccion_y.setter
    def distancia_deteccion_y(self, value):
        self._distancia_deteccion_y = value
        
    @property
    def movimiento_detectado(self):
        return self._movimiento_detectado
    @movimiento_detectado.setter
    def movimiento_detectado(self, value):
        self._movimiento_detectado = value

    # métodos específicos del sensor de movimiento    
    def leer_datos(self) -> dict[str, any]:
        movimiento_detectado = False
        movimiento_detectado = random.random() < 0.3 # 30% de probabilidad de detectar movimiento
        
        if movimiento_detectado:
            self._contador_movimientos = 1
            self._ultimo_movimiento = datetime.now()
            self._historial.append(self._ultimo_movimiento)
            self._distancia_deteccion_x = random.uniform(self._radio_cobertura*-1, self._radio_cobertura)
            self._distancia_deteccion_y = random.uniform(self._radio_cobertura*-1, self._radio_cobertura)
        else:
            self._distancia_deteccion_x = None
            self._distancia_deteccion_y = None

        datos = {
            "movimiento_detectado": movimiento_detectado,
            "distancia_deteccion_x": self._distancia_deteccion_x,
            "distancia_deteccion_y": self._distancia_deteccion_y,
        }
        return datos
    
    def procesar_datos(self, datos):
        msg = "No se detectó movimiento."
        direccion_x = None
        direccion_y = None
        distancia = None

        if datos["movimiento_detectado"]:
            distancia = (datos["distancia_deteccion_x"]**2 ,datos["distancia_deteccion_y"]**2)**0.5   # Teorema de Pitágoras
            if datos["distancia_deteccion_x"] > 0:
                direccion_x = "derecha"
            elif datos["distancia_deteccion_x"] < 0:
                direccion_x = "izquierda"
            if datos["distancia_deteccion_y"] > 0:
                direccion_y = "alfrente"
            elif datos["distancia_deteccion_y"] < 0:
                direccion_y = "atrás"

            msg = f"Movimiento detectado a {distancia:.2f} metros, {direccion_y} y a la {direccion_x}."

        return msg