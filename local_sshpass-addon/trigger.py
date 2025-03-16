#!/usr/bin/env python3
import os
import subprocess
import paho.mqtt.client as mqtt

MQTT_BROKER = os.environ.get("MQTT_BROKER", "core-mosquitto")
MQTT_PORT = int(os.environ.get("MQTT_PORT", "1883"))
MQTT_TOPIC = os.environ.get("MQTT_TOPIC", "local_sshpass-addon/trigger")

SSH_PASS = os.environ.get("SSH_PASS")  # Wird über den Supervisor konfiguriert
TARGET_IP = os.environ.get("TARGET_IP")  # Ebenso
PYTHON_PATH = os.environ.get("PYTHON_PATH", "/root/ls_tc_scraper/venv/bin/python")
PYTHON_SCRIPT = os.environ.get("PYTHON_SCRIPT", "/root/ls_tc_scraper/ls_tc_scraper.py")
STOCK_URL = os.environ.get("STOCK_URL", "https://www.beispielseite.de/aktie/tesla-motors-aktie")
STOCK_NAME = os.environ.get("STOCK_NAME", "Tesla Motors Aktie")

ssh_command = (
    f"/usr/bin/sshpass -p '{SSH_PASS}' ssh -o StrictHostKeyChecking=no root@{TARGET_IP} "
    f"'{PYTHON_PATH} {PYTHON_SCRIPT} \"{STOCK_URL}\" \"{STOCK_NAME}\"'"
)

def on_connect(client, userdata, flags, rc):
    print("Verbunden mit MQTT, RC:", rc)
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    print("Nachricht empfangen auf", msg.topic, ":", msg.payload.decode())
    try:
        result = subprocess.run(ssh_command, shell=True, check=True, capture_output=True, text=True)
        print("Ausgabe des Befehls:", result.stdout)
    except subprocess.CalledProcessError as e:
        print("Fehler beim Ausführen des Befehls:", e, e.stderr)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_forever()
