import paho.mqtt.client as paho
import serial
import time
import numpy as np
# XBee setting
serdev = '/dev/ttyUSB0'
s = serial.Serial(serdev, 9600)

s.write("+++".encode())
char = s.read(2)
print("Enter AT mode.")
print(char.decode())

s.write("ATMY 0x122\r\n".encode())
char = s.read(3)
print("Set MY 0x122.")
print(char.decode())

s.write("ATDL 0x222\r\n".encode())
char = s.read(3)
print("Set DL 0x222.")
print(char.decode())

s.write("ATID 0x1\r\n".encode())
char = s.read(3)
print("Set PAN ID 0x1.")
print(char.decode())

s.write("ATWR\r\n".encode())
char = s.read(3)
print("Write config.")
print(char.decode())

s.write("ATMY\r\n".encode())
char = s.read(4)
print("MY :")
print(char.decode())

s.write("ATDL\r\n".encode())
char = s.read(4)
print("DL : ")
print(char.decode())

s.write("ATCN\r\n".encode())
char = s.read(3)
print("Exit AT mode.")
print(char.decode())

print("start sending RPC")
v = []
# send RPC to remote
s.write("/GetVelocity/run\r".encode())
for i in range(30):
    velocity = float(s.readline())
    print(velocity)
    v.append(velocity)

# MQTT
mqttc = paho.Client()

host = "192.168.43.207"
topic = "velocity"

# Callbacks
def on_connect(self, mosq, obj, rc):
      print("Connected rc: " + str(rc))

def on_message(mosq, obj, msg):
      print("[Received] Topic: " + msg.topic + ", Message: " + str(msg.payload) + "\n")

def on_subscribe(mosq, obj, mid, granted_qos):
      print("Subscribed OK")

def on_unsubscribe(mosq, obj, mid, granted_qos):
      print("Unsubscribed OK")

# Set callbacks
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe
mqttc.on_unsubscribe = on_unsubscribe

# Connect and subscribe
print("Connecting to " + host + "/" + topic)
mqttc.connect(host, port=1883, keepalive=60)
mqttc.subscribe(topic, 0)

# Publish messages from Python
num = 0
while num != 30:
      ret = mqttc.publish(topic, str(v[num]) + "\n", qos=0)
      if (ret[0] != 0):
            print("Publish failed")
      mqttc.loop()
      time.sleep(0.5)
      num += 1
s.close()