from __future__ import annotations
import random
from rich.console import Console
from rich.panel import Panel
from rich.rule import Rule
from rich.table import Table
import pyfiglet
from core.iot_game import IoTSecurityGame

console = Console()

def mostrar_banner():
    ascii_banner = pyfiglet.figlet_format("IoT Security Game")
    console.print(Panel.fit(
        f"[bold cyan]{ascii_banner}[/bold cyan]",
        border_style="magenta",
        subtitle="[green]Seguridad en tus manos 🚀[/green]",
        subtitle_align="right"
    ))
    console.print(Rule("[bold yellow] Bienvenido al simulador de seguridad IoT [/bold yellow]"))

def mostrar_instrucciones():
    instrucciones = (
        "[cyan]1.[/cyan] Elige un dispositivo IoT.\n"
        "[cyan]2.[/cyan] Observa el impacto en la red.\n\n"
        "[bold green]¡Tu objetivo es proteger todos los dispositivos![/bold green]"
    )
    console.print(Panel(instrucciones, title="[bold magenta]Instrucciones[/bold magenta]", border_style="cyan"))

def main():
    random.seed()
    mostrar_banner()
    mostrar_instrucciones()
    game = IoTSecurityGame()
    game.play()

if __name__ == "__main__":
    main()
