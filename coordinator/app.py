import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from strategies import ConsistencyManager, NODES
from monitor import AvailabilityMonitor
import os

app = Flask(__name__)
CORS(app) # allow dashboard to see API

monitor = AvailabilityMonitor()
manager = ConsistencyManager()

# Global config toggled via environment or API
MODE = os.getenv("MODE", "STRONG") # Options: STRONG, EVENTUAL, WEAK

# Global variable to store nodeIDs
NODE_ID = os.getenv("NODE_ID", "unknown_node")

@app.route('/stats')
def stats():
    return jsonify({
        "mode": MODE,
        "uptime_percent": f"{monitor.get_uptime_percentage():.4f}%",
        "sla_status": monitor.get_sla_status(),
        "total_reqs": monitor.total_requests
    })

@app.route('/data', methods=['POST'])
def handle_write():
    key = request.json.get('key')
    val = request.json.get('value')
    
    success = False
    if MODE == "STRONG":
        success = manager.write_strong(key, val)
    elif MODE == "EVENTUAL":
        success = manager.write_eventual(key, val)
    elif MODE == 'QUORUM': # another fix
        success = manager.write_quorum(key, val)
    monitor.record(success)
    return jsonify({"success": success, "mode": MODE}), 200 if success else 500

@app.route('/data/<key>')
def handle_read(key):
    # Active-Active: try nodes until one responds
    for node in NODES:
        try:
            # changed from requests to request
            r = requests.get(f"{node}/get/{key}", timeout=0.5)
            if r.status_code == 200:
                return r.json()
        except Exception:
            continue
    return jsonify({"error": "Data Unavailable"}), 503

# change model between strong, eventual, and quorum
@app.route('/mode', methods=['POST'])
def set_mode():
    global MODE
    new_mode = request.json.get('mode')
    if new_mode in ["STRONG", "EVENTUAL", "QUORUM"]:
        MODE = new_mode
        return jsonify({"status": "mode updated", "current_mode": MODE})
    return jsonify({"error": "Invalid mode"}), 400

@app.route('/health')
def health_check():
    status = {}
    # Map the long container names to the short IDs the JS expects
    mapping = {
        "node-1": "http://node-1:8000",
        "node-2": "http://node-2:8000",
        "node-3": "http://node-3:8000"
    }
    for short_name, url in mapping.items():
        try:
            # issue was here with requests
            r = requests.get(f"{url}/get/health", timeout=0.2)
            status[short_name] = "online" if r.status_code == 200 else "offline"
        except Exception:
            status[short_name] = "offline"
    return jsonify(status)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)

