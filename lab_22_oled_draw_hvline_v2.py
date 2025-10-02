#lab_22_oled_draw_hvline_v2.py
from machine import Pin, SoftI2C
import ssd1306
import time

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

# fill
#text
oled.text("Draw HV Line", 15, 5) # ("text", X, Y)

# Hline
oled.hline(1, 1, 127, 2) # (x, y, ยาว, หนา)
oled.hline(1, 15, 127, 2) # (x, y, ยาว, หนา)
oled.hline(1, 63, 127, 2) # (x, y, ยาว, หนา)

# Vline
oled.vline(1, 1, 63, 2) # (x, y, ยาว, หนา)
oled.vline(127, 1, 63, 2) # (x, y, ยาว, หนา)

#Text
oled.text("Draw HV Line 1", 8, 20) # ("text", X, Y)
oled.text("Draw HV Line 2", 8, 30) # ("text", X, Y)
oled.text("Draw HV Line 3", 8, 40) # ("text", X, Y)
oled.text("Draw HV Line 4", 8, 50) # ("text", X, Y)

oled.show()
time.sleep(1)