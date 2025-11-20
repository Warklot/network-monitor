import json
import logging
import os
import random
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
        # Simulate ping if running in GitHub Actions
        if os.getenv("CI") == "true":
            return {
                "status": random.choice(["up", "down"]),
                "latency": round(random.uniform(10, 50), 2)
            }
        # Local environment: real ping
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
        # Save JSON output for later review
        with open(filename, "w") as f:
            json.dump(results, f, indent=4)
        print(f"Results saved to {filename}")

if __name__ == "__main__":
    devices = [
        Device("Google DNS", "8.8.8.8"),
        Device("Cloudflare DNS", "1.1.1.1"),
        Device("GitHub", "github.com")
    ]
    monitor = NetworkMonitor(devices)
    monitor.save_results()
