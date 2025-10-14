from dataclasses import dataclass
from datetime import datetime

@dataclass
class Alert:
    device: any  # Replace with the actual type if known
    is_real: bool
    message: str
    severity: str
    timestamp: datetime