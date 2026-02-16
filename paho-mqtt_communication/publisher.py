import paho.mqtt.client as mqtt
import time
import json
import random

client = mqtt.Client(
    client_id="pod1_publisher",
    protocol=mqtt.MQTTv311,
    transport="tcp",
    userdata=None,
    callback_api_version=mqtt.CallbackAPIVersion.VERSION2
)

client.connect("broker.hivemq.com", 1883, 60)
client.loop_start()

try:
    while True:
        telemetry_data = {
        "pod_name": "Avishkar-1",
        "speed": random.randint(600, 900),
        "battery": random.randint(50, 100),
        "status": random.choice(["Operational", "Docked", "Maintenance"])
        }

        client.publish(
        topic="hyperloop/pod1/telemetry",
        payload=json.dumps(telemetry_data),
        qos=1,
        retain=False
        )

        print("Published:", telemetry_data)
        time.sleep(2)
    
except KeyboardInterrupt:
    client.loop_stop()
    client.disconnect()

