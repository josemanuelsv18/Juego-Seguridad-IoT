from dataclasses import dataclass
import random
from datetime import datetime

@dataclass
class Device:
    id: int
    name: str
    type: str
    base_real_prob: float  # probabilidad base de alerta real (0..1)

    def generate_alert(self, current_hour: int) -> "Alert":
        hour_factor = 1.0
        if 7 <= current_hour <= 22:
            hour_factor = 1.1
        else:
            hour_factor = 0.9
        prob_real = min(max(self.base_real_prob * hour_factor, 0.05), 0.95)
        is_real = random.random() < prob_real
        severity = random.choice(["Baja", "Media", "Alta"])
        msg = f"{self.type} reporta {'actividad' if is_real else 'un falso positivo'}."
        return Alert(device=self, is_real=is_real, message=msg, severity=severity, timestamp=datetime.now())

@dataclass
class Alert:
    device: Device
    is_real: bool
    message: str
    severity: str
    timestamp: datetime