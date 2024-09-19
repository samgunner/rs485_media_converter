import serial
import paho.mqtt.client as mqtt
import random
import ssl
from datetime import datetime
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--debug", help="print sent and received messages",
                    action="store_true")
parser.add_argument("-l", "--location", type=str, choices=['battery', 'meter'],
                    help="the RS485 connection this devices has")

args = parser.parse_args()
location = args.location
DEBUG = args.debug

## SETTIGN UP SERIAL
ser = serial.Serial(
        # Serial Port to read the data from
        port='/dev/ttyAMA0',
 
        #Rate at which the information is shared to the communication channel
        baudrate = 9600,
   
        #Applying Parity Checking (none in this case)
        parity=serial.PARITY_NONE,
 
       # Pattern of Bits to be read
        stopbits=serial.STOPBITS_ONE,
     
        # Total number of bits to be read
        bytesize=serial.EIGHTBITS,
 
        # Number of serial commands to accept before timing out
        timeout=0.05
)

## SETTING UP MQTT
base_topic = 'bat_meter/'
topic_responce = base_topic+'responce'
topic_request = base_topic+'request'

broker_address = "192.168.1.78"
broker_port = 1883

# different locations need different topics 
if location == 'meter':
    send_topic = topic_responce
    receive_topic = topic_request
elif location == 'battery':
    send_topic = topic_request
    receive_topic = topic_responce
else:
    print('Error: location must be either \'meter\' or \'battery\'')
    exit(1)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code", rc)
    client.subscribe(receive_topic)

# when we recieve an MQTT message we send the payload to the RS485
def on_message(client, userdata, msg):
    ser.write(msg.payload)
    if DEBUG:
        print('{}: {} - {} : eth->RS485'.format(datetime.now().isoformat(), msg.topic, msg.payload))


mytransport = 'tcp'

client = mqtt.Client(client_id=f'python-mqtt-{random.randint(0, 1000)}',
                     transport=mytransport,
                     protocol=mqtt.MQTTv311
                     )
client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set(username="bat_meter", password='B4t_M3t3r')
print("Connecting...")
client.connect(broker_address, broker_port)
client.loop_start()

# Start a never ending loop reading in the RS485 and publishing anything that arries to the broker
while 1:
        msg=ser.readline()
        if msg != b'':
            client.publish(send_topic, msg)
            if DEBUG:
                print('{}: {} - {} : RS485->eth'.format(datetime.now().isoformat(), send_topic, msg))
                

