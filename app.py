from flask import Flask, jsonify, request
from monitor import Device, NetworkMonitor

app = Flask(__name__)

devices = []
monitor = NetworkMonitor(devices)

@app.route("/health", methods=["GET"])
def health_check():
    results = monitor.run_checks()
    return jsonify(results)

@app.route("/health/<device_name>", methods=["GET"])
def device_health(device_name):
    for device in devices:
        if device.name.lower() == device_name.lower():
            return jsonify({device.name: device.check_health()})
    return jsonify({"error": "Device not found"}), 404

@app.route("/devices", methods=["POST"])
def add_device():
    data = request.get_json()
    name = data.get("name")
    ip = data.get("ip")
    if not name or not ip:
        return jsonify({"error": "Missing 'name' or 'ip'"}), 400

    for d in devices:
        if d.name.lower() == name.lower():
            return jsonify({"error": "Device already exists"}), 400

    new_device = Device(name, ip)
    devices.append(new_device)
    return jsonify({"message": f"Device '{name}' added successfully."}), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
