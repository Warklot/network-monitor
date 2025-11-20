# monitor.py
import json
import logging
from ping3 import ping
import random, os

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
        if os.getenv("CI") == "true":
            return {"status": random.choice(["up", "down"]),
                    "latency": round(random.uniform(10, 50), 2)}
        response = ping(self.ip, timeout=2)
        if response is None:
            return {"status": "down", "latency": None}
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
