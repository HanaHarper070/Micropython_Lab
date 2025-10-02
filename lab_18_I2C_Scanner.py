# lab_18_I2C_Scanner.py
from machine import Pin, SoftI2C

i2c = SoftI2C(scl=Pin(5), sda=Pin(4)) #rp picow

print('I2C SCANNER')
devices = i2c.scan()

if len(devices) == 0:
	print("No i2c device !")
else:
	print('i2c devices found:', len(devices))

	for device in devices:
		print("I2C hexadecimal address: ", hex(device))