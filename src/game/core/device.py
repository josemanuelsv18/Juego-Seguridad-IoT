from dataclasses import dataclass
import random
from datetime import datetime
from core.alert import Alert  # <-- use the shared Alert type

@dataclass
class Device:
    id: int
    name: str
    type: str
    base_real_prob: float  # probabilidad base de alerta real (0..1)

    def generate_alert(self, current_hour: int) -> Alert:
        hour_factor = 1.0
        if 7 <= current_hour <= 22:
            hour_factor = 1.7
        else:
            hour_factor = 0.9
        prob_real = min(max(self.base_real_prob * hour_factor, 0.05), 0.95)
        rnd = random.random()
        # Debug temporal: muestra probabilidad y el valor aleatorio
       # print(f"[DEBUG] prob_real={prob_real:.4f}, random={rnd:.4f}")
        is_real = rnd < prob_real
        #print(f" real dice true?: {is_real}")
        severity = random.choice(["Baja", "Media", "Alta"])
        msg = f"{self.type} reporta actividad."
        return Alert(device=self, is_real=is_real, message=msg, severity=severity, timestamp=datetime.now())