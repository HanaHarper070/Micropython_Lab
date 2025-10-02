#lab34_DS18B20_BH1750_DHT22_SoilMC_ESP32.py
from ds18x20 import DS18X20
from machine import Pin, SoftI2C, ADC
from onewire import OneWire
from bh1750 import BH1750
import dht
from time import sleep 

# Initialize I2C communication (ESP32)
#i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=400000)
i2c = SoftI2C(scl=Pin(5), sda=Pin(4))

#Create DS18b20 object
ds18b20_pin = Pin(27) # rp pico board
ds18b20_sensor = DS18X20(OneWire(ds18b20_pin))
roms = ds18b20_sensor.scan()
print('Found DS devices: ', roms)

# Create BH1750 object
light_sensor = BH1750(bus=i2c, addr=0x23)

# Create DHT22 object
sensor = dht.DHT22(Pin(14))

# Configure ADC for SoilMC
soil = ADC(Pin(34))
soil.width(ADC.WIDTH_10BIT)
soil.atten(ADC.ATTN_11DB)

####### Caribration #######
soil_value_max = 600
soil_value_min = 100
####### Caribration #######

while True:
	sleep(1)
	
	#DHT22
	sensor.measure()
	temp = sensor.temperature()
	hum = sensor.humidity()
	print('Temperature: %3.1f C' %temp)
	print('Humidity: %3.1f %%' %hum)
	
	#SoilMC
	soil_value = soil.read()
	#print(soil_value)
	percent_soil_value = int((soil_value_max-soil_value)*100/(soil_value_max-soil_value_min))
	print(f'status percent_soil_value: {percent_soil_value}')
	
	#SD18B20
	ds18b20_sensor.convert_temp()
	sleep(0.750)
	for rom in roms:
		#print(rom)
		ds18b20_temp = ds18b20_sensor.read_temp(rom)
		ds18b20_temp = round(ds18b20_temp, 2)
		print('Temperature_ds18b20: %3.2f C' %ds18b20_temp)
	
	#BH1750
	lux = light_sensor.luminance(BH1750.CONT_HIRES_1)
	lux = round(lux, 2)
	print(f"Light Luminance: {lux} lux")
	print('* '*20)
	sleep(1)