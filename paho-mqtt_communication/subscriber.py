import paho.mqtt.client as mqtt
import time

def on_message(client, userdata, msg):
    print("Received:", msg.payload.decode())

client = mqtt.Client(
    client_id="subscriber1",
    protocol=mqtt.MQTTv311,
    transport="tcp",
    userdata=None,
    callback_api_version=mqtt.CallbackAPIVersion.VERSION2
)

client.on_message = on_message

client.connect("broker.hivemq.com", 1883, 60)
client.subscribe("hyperloop/+/telemetry")

client.loop_start()

try:
    while True:
        print("Streamlit can be integrated next....")
        time.sleep(5)

except KeyboardInterrupt:
    client.loop_stop()
    client.disconnect()

