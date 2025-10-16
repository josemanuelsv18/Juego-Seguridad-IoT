import random
from typing import List, Optional
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.live import Live
from rich.prompt import Prompt
from core.device import Device
from core.alert import Alert 
from utils.enums.tipo_dispositivo import TipoDispositivo   

console = Console()

class IoTSecurityGame:
    ROUNDS = 5
    START_POINTS = 15

    def __init__(self, devices: Optional[List[Device]] = None):
        if devices is None:
            self.devices = self._default_devices()
        else:
            self.devices = devices
        self.points = self.START_POINTS
        self.round_no = 0

    def _default_devices(self) -> List[Device]:
        return [
            Device(1, "Camara Principal", TipoDispositivo.CAMARA.value, random.random()),
            Device(2, "Sensor Puerta", TipoDispositivo.CERRADURA.value, random.random()),
            Device(3, "Sensor Movimiento Sala", TipoDispositivo.SENSOR_MOVIMIENTO.value, random.random()),
            Device(4, "Sensor Temperatura", TipoDispositivo.SENSOR_TEMPERATURA.value, random.random()),
            Device(5, "Router Oficina", TipoDispositivo.ROUTER.value, random.random()),
            Device(6, "Sensor RFID Entrada", TipoDispositivo.SENSOR_RFID.value, random.random()),
            Device(7, "Sensor Ruido", TipoDispositivo.SENSOR_RUIDO.value, random.random())
        ]

    def _render_header(self) -> Panel:
        text = f"[bold yellow]Examen Parcial #2 - Desarrollo de Software VIII[/]\n[bold]Ronda[/] {self.round_no}/{self.ROUNDS}  •  [bold]Puntos[/] {self.points}"
        return Panel(text, title="Juego: Seguridad IoT", subtitle="Administra las alertas")

    def _alerts_table(self, alerts: List[Alert]) -> Table:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Índice", style="bold")
        table.add_column("Dispositivo")
        table.add_column("Tipo")
        table.add_column("Hora")
        table.add_column("Severidad")
        table.add_column("Mensaje")
        table.add_column("Prob. Real (estimada)")
        for i, a in enumerate(alerts, start=1):
            prob_est = f"{int(a.device.base_real_prob * 100)}%"
            time_str = a.timestamp.strftime("%H:%M:%S")
            table.add_row(str(i), a.device.name, a.device.type, time_str, a.severity, a.message, prob_est)
        return table

    def _ask_user_selection(self, alerts: List[Alert]) -> List[int]:
        raw = Prompt.ask("[bold]Atender alertas[/]", default="")
        if not raw.strip():
            return []
        indices = []
        for token in raw.split(","):
            token = token.strip()
            if not token:
                continue
            if token.isdigit():
                idx = int(token)
                if 1 <= idx <= len(alerts):
                    indices.append(idx)
                else:
                    console.print(f"[red]Índice fuera de rango: {token}. El índice debe estar entre 1 y {len(alerts)}.[/]")
            else:
                console.print(f"[red]Entrada inválida: {token}. Asegúrate de ingresar solo números.[/]")
        return sorted(set(indices))

    def _score_round(self, alerts: List[Alert], attended_indices: List[int]):
        for idx in attended_indices:
            try:
                alert = alerts[idx - 1]  
                if alert.is_real:
                    self.points += 2
                else:
                    self.points -= 2
            except IndexError as e: 
                console.print(f"[red]¡Error! Índice fuera de rango: {idx}. No se encuentra en la lista de alertas.[/]")
            except Exception as e: 
                console.print(f"[red]Se ha producido un error inesperado: {e}[/]")

        if self.points < 0:
            self.points = 0

    def play(self):
        console.clear()
        console.rule("[bold blue]Juego: Seguridad IoT")
        console.print()
    
        for r in range(1, self.ROUNDS + 1):
            self.round_no = r
            current_hour = random.randint(0, 23)
            alerts = [d.generate_alert(current_hour) for d in self.devices]
  
            # Mostrar cabecera y tabla
            console.print(self._render_header())
            table = self._alerts_table(alerts)
            console.print(Panel(table, title=f"Alertas - Ronda {r}"))
            console.print()

            # Pedir al usuario que seleccione alertas
            attended = self._ask_user_selection(alerts)
            self._score_round(alerts, attended)

            # Mostrar el resumen de la ronda
            summary = Table.grid(padding=1)
            summary.add_column()
            summary.add_row(f"Puntos después de la ronda: [bold]{self.points}[/]")
            summary.add_row(f"Atendiste {len(attended)} alerta(s).")
            console.print(Panel(summary, title="Resumen de ronda"))
            
            console.print("\n[dim]Presiona Enter para continuar a la siguiente ronda...[/]")
            input()
            
            # Limpiar antes de la siguiente ronda
            if r < self.ROUNDS:
                console.clear()

        # Mensaje final
        console.clear()
        result_message = (
            "[green]¡Victoria! Has terminado con 15 o más puntos.[/]"
            if self.points >= 15
            else "[red]Derrota. Terminaste con menos de 15 puntos.[/]"
        )
        result_panel = Panel.fit(
            f"Puntuación final: [bold]{self.points}[/]\n\n{result_message}",
            title="Fin del Juego"
        )
        console.print(result_panel)
