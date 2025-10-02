#lab_19_oled_draw_hline.py
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
#oled.fill(1)
oled.text("Draw Line", 10, 5) # ("text", X, Y)
oled.show()
time.sleep(1)

# Hline
oled.hline(1, 1, 127, 2) # (x, y, ยาว, หนา)
oled.show()
time.sleep(1)

# Hline
oled.hline(1, 15, 127, 2) # (x, y, ยาว, หนา)
oled.show()
time.sleep(1)

# Hline
oled.hline(1, 63, 127, 2) # (x, y, ยาว, หนา)
oled.show()
time.sleep(1)