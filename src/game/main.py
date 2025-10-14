from __future__ import annotations
import random
from pathlib import Path
from rich.console import Console
from rich.prompt import Prompt
from core.iot_game import IoTSecurityGame 

console = Console()

def main():
    random.seed()  # opcional: parametrizar si quieres reproducibilidad
    game = IoTSecurityGame()
    game.play()

if __name__ == "__main__":
    main()