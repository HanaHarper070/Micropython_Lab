#lab_19_oled_i2c.py
from machine import Pin, SoftI2C
import ssd1306
from time import sleep

#i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
i2c = SoftI2C(scl=Pin(5), sda=Pin(4))

oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

# add text
oled.text('Hello, World 1!', 5, 10) # (text, X,Y)
oled.text('Hello, World 2!', 5, 30)
oled.text('Hello, World 3!', 5, 50)
oled.show()