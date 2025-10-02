#lab_18_Scane_I2C_v1.py
from machine import Pin, SoftI2C
import ssd1306

i2c = SoftI2C(scl=Pin(5), sda=Pin(4))
#i2c = SoftI2C(scl=Pin(22), sda=Pin(21))

print('I2C SCANNER')
devices = i2c.scan()

if len(devices) == 0:
	print("No i2c device !")
else:
	print('i2c devices found:', len(devices))

	for device in devices:
		print("I2C hexadecimal address: ", hex(device))

oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

# add text
oled.text("Hello, jack01", 10, 10) # ("text", X, Y)
oled.text("Hello, jack02", 10, 20) # ("text", X, Y)
oled.text("Hello, jack03", 10, 30) # ("text", X, Y)
oled.text("Hello, jack04", 10, 40) # ("text", X, Y)
oled.text("Hello, jack05", 10, 50) # ("text", X, Y)
oled.show()