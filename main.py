import mqtt
import network
import timer
import time
import machine
import ubinascii
import bme280

UID = ubinascii.hexlify(machine.unique_id()).decode()
I2C = machine.I2C(sda=machine.Pin(21), scl=machine.Pin(22))
BME = bme280.BME280(i2c=I2C)

def init_wifi():
	nic = network.WLAN(network.STA_IF)
	nic.active(True)
	nic.connect("CCCAC_OPEN_2.4GHz", None)

	while not nic.isconnected():
		time.sleep_ms(100)
	print("WIFI connection established")

def init_mqtt(mqtt):
	mqtt.connect()
	print("MQTT connection established")

def publish_sensor():
	(temperature, pressure, humidity) = BME.values
	m.publish("sensors/{}/temperature".format(UID), str(temperature))
	m.publish("sensors/{}/pressure".format(UID), str(pressure))
	m.publish("sensors/{}/humidity".format(UID), str(humidity))
	print("{}\t{}\t{}".format(temperature, pressure, humidity))
	tmr.add(1000, publish_sensor)

print("Boot complete")
m = mqtt.MQTTClient("Sensor_{}".format(UID), "mqtt.space.aachen.ccc.de")
tmr = timer.Timer(100)

init_wifi()
init_mqtt(m)

tmr.add(1000, publish_sensor)
tmr._start()
