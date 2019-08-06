import mqtt
import network
import timer
import time
import machine
import ubinascii
import bme280
import scd30
import max7219

UID = ubinascii.hexlify(machine.unique_id()).decode()
I2C = machine.I2C(sda=machine.Pin(21), scl=machine.Pin(22))
BME = bme280.BME280(i2c=I2C)
SCD = scd30.SCD30(I2C)
LED = max7219.max7219()
LED.set_intensity(max7219.INTENSITY_15)

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

def publish_bme280():
	try:
		(temperature, pressure, humidity) = BME.values
	except:
		pass
	else:
		m.publish("sensors/{}/temperature".format(UID), str(temperature))
		m.publish("sensors/{}/pressure".format(UID), str(pressure))
		m.publish("sensors/{}/humidity".format(UID), str(humidity))
		#print("{}\t{}\t{}".format(temperature, pressure, humidity))
	finally:
		tmr.add(1000, publish_bme280)

def read_scd30():
	try:
		SCD.read()
	except SyntaxError as e:
		pass
	finally:
		tmr.add(2000, read_scd30)

def publish_scd30():
	try:
		(co2, temperature, humidity) = SCD.values()
	except Exception as e:
		pass
	else:
		m.publish("sensors/{}/scd30/co2".format(UID), str(co2))
		m.publish("sensors/{}/scd30/temperature".format(UID), str(temperature))
		m.publish("sensors/{}/scd30/humidity".format(UID), str(humidity))
		#print("{}\t{}\t{}".format(temperature, pressure, humidity))
		LED.write_string("CO2{: >5}".format(int(co2)))
	finally:
		tmr.add(2000, publish_scd30)

def print_scd30():
	try:
		(co2, temperature, humidity) = SCD.values()
	except Exception as e:
		pass
	else:
		LED.write_string("CO2{: >5}".format(int(co2)))
	finally:
		tmr.add(2000, print_scd30)

print("Boot complete")
#m = mqtt.MQTTClient("Sensor_{}".format(UID), "mqtt.space.aachen.ccc.de")
tmr = timer.Timer(100)

#init_wifi()
#init_mqtt(m)

#tmr.add(1000, publish_bme280)
#tmr.add(2333, publish_scd30)
tmr.add(2100, print_scd30)
tmr._start()
