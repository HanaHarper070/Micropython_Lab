#lab_20_oled_i2c_fill.py
from machine import Pin, SoftI2C
import ssd1306
from time import sleep

#i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
i2c = SoftI2C(scl=Pin(5), sda=Pin(4))

oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

# fill 
# oled.fill(1) #Entire screen with white
oled.fill(0) #Sets all pixels to black

oled.show()
