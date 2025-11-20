import json
import logging
from ping3 import ping

logging.basicConfig(
    filename="network_monitor.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class Device:
    def __init__(self, name, ip):
        self.name = name
        self.ip = ip

    def check_health(self):
        response = ping(self.ip, timeout=2)
        if response is None:
            return {"statsus": "down", "latency": None}
        return {"status": "up", "latency": round(response * 1000, 2)}

class NetworkMonitor:
    def __init__(self, devices):
        self.devices = devices

    def run_checks(self):
        results = {}
        for device in self.devices:
            results[device.name] = device.check_health()
        return results

    def save_results(self, filename="network_results.json"):
        results = self.run_checks()
        for device, data in results.items():
            logging.info(f"{device}: {data}")


if __name__ == "__main__":
    devices = [
        Device("Google DNS", "8.8.8.8"),
        Device("Cloudflare DNS", "1.1.1.1"),
        Device("GitHub", "github.com")
    ]
    monitor = NetworkMonitor(devices)
    monitor.save_results()
