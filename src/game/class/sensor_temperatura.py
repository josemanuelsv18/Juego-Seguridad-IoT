import random
from dispositivo import Dispositivo
from ..utils.enums.tipo_dispositivo import TipoDispositivo
from ..utils.enums.unidad_temperatura import UnidadTemperatura

class SensorTemperatura(Dispositivo):
    def __init__(self, nombre: str, ubicacion: str, unidad: UnidadTemperatura = UnidadTemperatura.CELSIUS):
        super().__init__(nombre, TipoDispositivo.SENSOR_TEMPERATURA, ubicacion)

        # Atributos específicos del sensor de temperatura
        self._unidad = unidad  # Unidad de medida (Celsius, Fahrenheit, Kelvin)
        self._temperatura_actual = None  # Temperatura actual medida
        self._temperatura_minima = None  # Temperatura mínima registrada
        self._temperatura_maxima = None  # Temperatura máxima registrada
        self._min_seguro = -30  # Temperatura mínima segura
        self._max_seguro = 50   # Temperatura máxima segura
        self._alerta_activada = False  # Indicador de alerta por temperatura fuera de rango

    # Getters y setters
    @property
    def unidad(self):
        return self._unidad
    @unidad.setter
    def unidad(self, value):
        self._unidad = value

    @property
    def temperatura_actual(self):
        return self._temperatura_actual
    @temperatura_actual.setter
    def temperatura_actual(self, value):
        self._temperatura_actual = value

    @property
    def temperatura_minima(self):
        return self._temperatura_minima
    @temperatura_minima.setter
    def temperatura_minima(self, value):
        self._temperatura_minima = value

    @property
    def temperatura_maxima(self):
        return self._temperatura_maxima
    @temperatura_maxima.setter
    def temperatura_maxima(self, value):
        self._temperatura_maxima = value

    @property
    def min_seguro(self):
        return self._min_seguro
    @min_seguro.setter
    def min_seguro(self, value):
        self._min_seguro = value

    @property
    def max_seguro(self):
        return self._max_seguro
    @max_seguro.setter
    def max_seguro(self, value):
        self._max_seguro = value

    @property
    def alerta_activada(self):
        return self._alerta_activada
    @alerta_activada.setter
    def alerta_activada(self, value):
        self._alerta_activada = value

    # Métodos específicos del sensor de temperatura
    def leer_datos(self):
        # Simular la lectura de temperatura entre -40 y 60 grados Celsius
        temp_normal = random.randint(0, 10)
        if temp_normal > 3: # 70% de probabilidad de estar en rango normal
            self._temperatura_actual = random.uniform(15, 25)
        else: # 30% de probabilidad de estar fuera de rango
            self._temperatura_actual = random.uniform(-40, 60)
        self._historial.append(self._temperatura_actual)

        

        return self._temperatura_actual
    
    def procesar_datos(self, datos, unidad: UnidadTemperatura = UnidadTemperatura.CELSIUS):
        if datos > self._max_seguro or datos < self._min_seguro:
            self._alerta_activada = True
        if self._temperatura_minima is None or datos < self._temperatura_minima:
            self._temperatura_minima = datos
        if self._temperatura_maxima is None or datos > self._temperatura_maxima:
            self._temperatura_maxima = datos
        
        u = "C°"
        if unidad != UnidadTemperatura.CELSIUS:
            if unidad == UnidadTemperatura.FAHRENHEIT:
                datos = (datos - 32) * 5.0/9.0
                u = "F°"
            elif unidad == UnidadTemperatura.KELVIN:
                datos = datos - 273.15
                u = "K"

        data = {

            "temperatura": round(datos, 2),
            "unidad": u,
            "alerta_activada": self._alerta_activada,
            "temperatura_minima": self._temperatura_minima,
            "temperatura_maxima": self._temperatura_maxima,
            "msg": f"{self.nombre} en {self.ubicacion}: Temperatura actual {round(datos,2)}{u}. Alerta activada: {self._alerta_activada}"
        }

        return data