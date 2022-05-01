import paho.mqtt.client as mqtt
import json
import os
import sys

environment = os.getenv('ENVIRONMENT','DEBUG')
channels_set = set()

if environment=='PRODUCTION':
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BOARD)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print(f'Connected with result code {rc}')

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe('/raspberrypi-pins/set')
    client.subscribe('/raspberrypi-pins/get')

def on_disconnect(client, userdata, rc):
    print(f'Disconnecting with result code {rc}')
    if environment=='PRODUCTION':
        GPIO.cleanup(list(channels_set))

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    if environment=='PRODUCTION':
        if msg.topic == '/raspberrypi-pins/set':
            try:
                pinInfo = json.loads(msg.payload)
                channels_set.add(pinInfo["channel"])
                if pinInfo["state"] == 'OUT':
                    GPIO.setup(pinInfo["channel"], GPIO.OUT)
                    GPIO.output(pinInfo["channel"], pinInfo["value"])
            except Exception as e:
                print(e)
        elif msg.topic == '/raspberrypi-pins/get':
            try:
                pinInfo = json.loads(msg.payload)
                if "value" not in pinInfo:
                    pinInfo["value"] = GPIO.input(pinInfo["channel"])
                    payload = json.dumps(pinInfo)
                    client.publish('/raspberrypi-pins/get', payload) 
            except Exception as e:
                print(e)
        

def main():
    try:
        print(f'App started in {environment} mode')
        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message
        client.on_disconnect = on_disconnect
        client.connect("localhost", 1883, 60)
        client.loop_forever()
    except (KeyboardInterrupt, SystemExit):
        print('Got SIGINT, gracefully shutting down')
        sys.exit()

if __name__ == "__main__":
    main()