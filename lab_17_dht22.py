#lab17_dht22.py
from machine import Pin
from time import sleep
import dht 

dht22 = dht.DHT22(Pin(14))

while True:
	try:
		sleep(2)
		dht22.measure()
		temp = dht22.temperature()
		hum = dht22.humidity()
		temp_f = temp * (9/5) + 32.0
		print('Temperature: %3.1f C' %temp)
		print('Temperature: %3.1f F' %temp_f)
		print('Humidity: %3.1f %%' %hum)
	except OSError as e:
		print('Failed to read sensor.')