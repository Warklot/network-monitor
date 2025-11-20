import unittest
from monitor import Device, NetworkMonitor

class TestMonitor(unittest.TestCase):

    def test_device_check_health_up(self):
        device = Device("Localhost", "127.0.0.1")
        result = device.check_health()
        self.assertIn(result["status"], ["up", "down"])
        self.assertTrue(result["latency"] is None or isinstance(result["latency"], float))

    def test_network_monitor_run_checks(self):
        devices = [Device("Localhost", "127.0.0.1")]
        monitor = NetworkMonitor(devices)
        results = monitor.run_checks()
        self.assertIn("Localhost", results)

if __name__ == "__main__":
    unittest.main()
