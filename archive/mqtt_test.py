import paho.mqtt.client as mqtt
import random
import ssl


def on_connect(client, userdata, flags, rc):
    print("Connected with result code", rc)
    client.subscribe("bat_meter/#")

def on_message(client, userdata, msg):
    print(msg.topic, msg.payload)


mytransport = 'tcp'

client = mqtt.Client(client_id=f'python-mqtt-{random.randint(0, 1000)}',
                     transport=mytransport,
                     protocol=mqtt.MQTTv311
                     )
client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set(username="bat_meter", password='B4t_M3t3r')
#client.tls_set(certfile=None,
#               keyfile=None,
#               cert_reqs=ssl.CERT_REQUIRED)
print("Connecting...")
client.connect("192.168.1.78", 1883)
client.loop_forever()
