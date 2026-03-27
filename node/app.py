from flask import Flask, request, jsonify
import time
import os

app = Flask(__name__)
storage = {}
NODE_ID = os.getenv("NODE_ID", "unknown")

@app.route('/get/<key>')
def get_val(key):
    # simulate a tiny network hop latency
    #time.sleep(0.05) 
    return jsonify({"node": NODE_ID, "val": storage.get(key), "status": "online"})

@app.route('/set', methods=['POST'])
def set_val():
    data = request.json
    storage[data['key']] = data['value']
    return jsonify({"status": "written", "node": NODE_ID})

@app.route('/get/health')
def health():
    return {"status": "online"}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)