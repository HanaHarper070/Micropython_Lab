#lab31_DS18B20_Temperature_Sensor.py
import machine, onewire, time
from ds18x20 import DS18X20

ds18b20_pin = machine.Pin(4)
ds18b20_sensor = DS18X20(onewire.OneWire(ds18b20_pin))

roms = ds18b20_sensor.scan() # scan for DS18B20 sensors. The addresses found are saved on the roms
print('Found DS devices: ', roms)

while True:
	ds18b20_sensor.convert_temp()
	time.sleep_ms(750)
	for rom in roms:
		print(rom)
		ds18b20_temp = ds18b20_sensor.read_temp(rom)
		ds18b20_temp = round(ds18b20_temp, 2)
		print('Temperature: %3.2f C' %ds18b20_temp)
		print('* '*20)
	time.sleep(1)