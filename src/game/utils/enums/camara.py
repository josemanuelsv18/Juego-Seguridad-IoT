from core.device import Device
import random
import datetime
from core.alert import Alert

# -----------------------------
# Subclases específicas
# -----------------------------

class Camera(Device):
    def __init__(self, id, name, base_real_prob):
        super().__init__(id, name, "Cámara", base_real_prob)

    def generate_alert(self, current_hour: int) -> Alert:
        """Cámaras son más sensibles de noche."""
        if 18 <= current_hour or current_hour < 6:
            factor = 2.0
        else:
            factor = 1.0
        prob_real = min(max(self.base_real_prob * factor, 0.05), 0.95)
        is_real = random.random() < prob_real
        severity = random.choice(["Media", "Alta"])
        msg = f"[CAM] {self.name} detecta movimiento inusual."
        return Alert(self, is_real, msg, severity, datetime.now())
