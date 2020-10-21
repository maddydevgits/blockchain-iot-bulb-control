import RPi.GPIO as gpio
import paho.mqtt.client as mqtt

client=mqtt.Client()
client.connect('broker.hivemq.com',1883)
client.subscribe('madblocks')

gpio.setmode(gpio.BCM)
gpio.setup(21,gpio.OUT)

def notification(client,userdata,msg):
	t=msg.payload
	t=t.decode('utf-8')
	if(t=='on'):
		gpio.output(21,1)
	elif(t=='off'):
		gpio.output(21,0)

client.on_message=notification
client.loop_forever()
