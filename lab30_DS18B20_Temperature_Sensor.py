#lab30_DS18B20_Temperature_Sensor.py
#import machine, onewire, ds18x20, time
import time
from machine import Pin
from onewire import OneWire
from ds18x20 import DS18X20
'''
ds18b20_pin = machine.Pin(27)
ds18b20_sensor = ds18x20.DS18X20(onewire.OneWire(ds18b20_pin))
'''
ds18b20_pin = Pin(27)
ds18b20_sensor = DS18X20(OneWire(ds18b20_pin))
roms = ds18b20_sensor.scan() # scan for DS18B20 sensors. The addresses found are saved on the roms
print('Found DS devices: ', roms)

while True:
	ds18b20_sensor.convert_temp()
	time.sleep_ms(750)
	for rom in roms:
		print(rom)
		print(ds18b20_sensor.read_temp(rom))
		print('* '*20)
	time.sleep(1)