import threading, time, json, requests
from flask import Flask, jsonify, render_template
import webview

app = Flask(__name__)
device_data = {}

def discover_devices(subnet_prefix="192.168.1."):
    devices = {}
    for i in range(1, 255):
        ip = f"{subnet_prefix}{i}"
        try:
            url = f"http://{ip}/cm?cmnd=Status%200"
            response = requests.get(url, timeout=0.5)
            if response.ok:
                data = response.json()
                if "StatusSNS" in data:
                    devices[ip] = data["StatusSNS"]
        except:
            continue
    return devices

def background_scanner():
    global device_data
    while True:
        device_data = discover_devices()
        time.sleep(10)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/devices")
def api_devices():
    return jsonify(device_data)

def start_flask():
    app.run(port=5000)

if __name__ == "__main__":
    # Стартиране на фоновия скенер
    threading.Thread(target=background_scanner, daemon=True).start()
    # Стартиране на Flask сървъра
    threading.Thread(target=start_flask, daemon=True).start()
    # Отваряне на десктоп прозорец с уеб интерфейс
    webview.create_window("SONOFF iPlug Monitor", "http://127.0.0.1:5000")
    webview.start()
