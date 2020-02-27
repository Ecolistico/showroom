#!/usr/bin/env python3

# Import directories
import socket
from time import time
from credentials import system
import paho.mqtt.publish as publish

class mqttController():
    def __init__(self):
        # Define aux variables
        self.clientConnected = False
        self.actualTime = time()

    # Function to display hostname and IP address
    def getIP(self):
        host_ip = ''
        try:
            host_name = socket.gethostname()
            host_ip = socket.gethostbyname(host_name)
        except:
            print("Unable to get Hostname and IP")
        return host_ip

    # Callback fires when conected to MQTT broker.
    def on_connect(self, client, userdata, flags, rc):
        Topic = "{}/Server".format(system['ID'])
        message = "MQTT"
        if(rc == 0):
            message += " Connection succesful"
            mssg = "Master connected"
            client.subscribe(Topic)
            print(message)
            print("Subscribed topic= {}".format(Topic))
        else:
            message += " Connection refused"
            if(rc == 1): message += " - incorrect protocol version"
            elif(rc == 2): message += " - invalid client identifier"
            elif(rc == 3): message += " - server unavailable"
            elif(rc == 4): message += " - bad username or password"
            elif(rc == 5): message += " - not authorised"
            else: message += " - currently unused"
            print(message)

    # Callback fires when a published message is received.
    def on_message(self, client, userdata, msg):
        top = msg.topic # Input Topic
        message = msg.payload.decode("utf-8") # Input message
        if message.startswith('whatIsMyIP'):
            IP = self.getIP()
            publish.single('{}/Server'.format(system['ID']), IP, hostname = system['brokerIP'])
            print('IP sent to master')

    # Callback fires when message published
    def on_publish(self, client, userdata, mid):
        print("Message delivered")

    # Callback fires when client disconnected
    def on_disconnect(self, client, userdata, rc):
        print("Client MQTT Disconnected")
        self.clientConnected = False
        self.actualTime = time()
