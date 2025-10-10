from enum import Enum

class TipoDispositivo(Enum):
    SENSOR_MOVIMIENTO = "Sensor de Movimiento"
    SENSOR_TEMPERATURA = "Sensor de Temperatura"
    SENSOR_ENERGIA = "Sensor de Energía"
    SENSOR_RFID = "Sensor RFID"
    SENSOR_RUIDO = "Sensor de Ruido"
    CAMARA = "Cámara"
    ROUTER = "Router"
    CERRADURA = "Cerradura"