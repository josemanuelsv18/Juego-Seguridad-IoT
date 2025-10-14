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
            Device(1, "Camara Principal", TipoDispositivo.CAMARA.value, 0.6),
            Device(2, "Sensor Puerta", TipoDispositivo.CERRADURA.value, 0.3),
            Device(3, "Sensor Movimiento Sala", TipoDispositivo.SENSOR_MOVIMIENTO.value, 0.5),
            Device(4, "Sensor Temperatura", TipoDispositivo.SENSOR_TEMPERATURA.value, 0.2),
            Device(5, "Router Oficina", TipoDispositivo.ROUTER.value, 0.4),
            Device(6, "Sensor RFID Entrada", TipoDispositivo.SENSOR_RFID.value, 0.35),
            Device(7, "Sensor Ruido", TipoDispositivo.SENSOR_RUIDO.value, 0.25)
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
        Prompt.ask("\n[cyan]Selecciona los índices (separados por comas) de las alertas que deseas atender.[/]\n")
       
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
                    indices.append(idx - 1)
                else:
                    console.print(f"[red]Índice fuera de rango ignorado:[/] {token}")
            else:
                console.print(f"[red]Entrada inválida ignorada:[/] {token}")
        return sorted(set(indices))

    def _score_round(self, alerts: List[Alert], attended_indices: List[int]):
        attended_set = set(attended_indices)
        for idx, alert in enumerate(alerts):
            attended = idx in attended_set
            if alert.is_real and attended:
                self.points += 2  # CORREGIDO: era = 2, debe ser += 2
            elif (not alert.is_real) and attended:
                self.points -= 1
            elif alert.is_real and not attended:
                self.points -= 2
        if self.points < 0:
            self.points = 0

    def play(self):
        console.clear()
        console.rule("[bold blue]Juego: Seguridad IoT")
        for r in range(1, self.ROUNDS + 1):
            self.round_no = r
            current_hour = random.randint(0, 23)
            alerts = [d.generate_alert(current_hour) for d in self.devices]

            with Live(auto_refresh=False) as live:
                live.update(self._render_header())
                table = self._alerts_table(alerts)
                live.update(Panel(table, title=f"Alertas - Ronda {r}"), refresh=True)

                attended = self._ask_user_selection(alerts)
                self._score_round(alerts, attended)

                summary = Table.grid(padding=1)
                summary.add_column()
                summary.add_row(f"Puntos después de la ronda: [bold]{self.points}[/]")
                summary.add_row(f"Atendiste {len(attended)} alerta(s).")
                live.update(Panel(summary, title="Resumen de ronda"), refresh=True)

            console.print("\n[dim]Presiona Enter para continuar a la siguiente ronda...[/]")
            input()

        # CORREGIDO: Panel final movido fuera del loop
        result_message = (
            "[green]¡Victoria! Has terminado con 15 o más puntos.[/]" 
            if self.points >= 15 
            else "[red]Derrota. Terminaste con menos de 15 puntos.[/]"
        )
        result_panel = Panel.fit(
            f"Puntuación final: [bold]{self.points}[/]\n\n{result_message}",
            title="Fin del Juego"
        )
        console.clear()
        console.print(result_panel)