from src.game.core.iot_game import IoTSecurityGame
from src.game.core.device import Device
from src.game.core.alert import Alert
import unittest
from datetime import datetime

class TestIoTSecurityGame(unittest.TestCase):

    def setUp(self):
        self.device = Device(id=1, name="Test Device", type="Sensor", base_real_prob=0.5)
        self.alert = self.device.generate_alert(current_hour=12)
        self.game = IoTSecurityGame(devices=[self.device])

    def test_device_alert_generation(self):
        self.assertIsInstance(self.alert, Alert)
        self.assertEqual(self.alert.device, self.device)
        self.assertIn(self.alert.severity, ["Baja", "Media", "Alta"])
        self.assertIsInstance(self.alert.timestamp, datetime)

    def test_game_initialization(self):
        self.assertEqual(self.game.points, IoTSecurityGame.START_POINTS)
        self.assertEqual(len(self.game.devices), 1)

    def test_score_round_real_alert_attended(self):
        self.game._score_round([self.alert], [0])  # Attending the alert
        self.assertEqual(self.game.points, IoTSecurityGame.START_POINTS , 2)

    def test_score_round_false_alert_attended(self):
        false_alert = Alert(device=self.device, is_real=False, message="Falso positivo", severity="Baja", timestamp=datetime.now())
        self.game._score_round([false_alert], [0])  # Attending the false alert
        self.assertEqual(self.game.points, IoTSecurityGame.START_POINTS - 1)

    def test_score_round_real_alert_not_attended(self):
        self.game._score_round([self.alert], [])  # Not attending the alert
        self.assertEqual(self.game.points, IoTSecurityGame.START_POINTS - 2)

if __name__ == '__main__':
    unittest.main()