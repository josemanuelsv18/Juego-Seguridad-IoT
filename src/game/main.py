from __future__ import annotations
import random
from rich.console import Console
from rich.panel import Panel
from rich.rule import Rule
from rich.table import Table
from core.iot_game import IoTSecurityGame

console = Console()

def main():
    random.seed()
    game = IoTSecurityGame()
    game.play()

if __name__ == "__main__":
    main()
