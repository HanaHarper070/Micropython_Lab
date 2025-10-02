#lab_21_oled_i2c_draw.py
from machine import Pin, SoftI2C
import ssd1306
from time import sleep

#i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
i2c = SoftI2C(scl=Pin(5), sda=Pin(4))

oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

# Draw a pixel
oled.pixel(0, 0, 1) # (X,Y, Pixel color) 
# 0 = black
# 1 = white

#oled.hline(5, 5, 30, 1)               # draw horizontal line x=0, y=8, width=4, colour=1
#oled.vline(10, 10, 45, 1)               # draw vertical line x=0, y=8, height=4, colour=1
#oled.line(0, 0, 127, 63, 1)          # draw a line from 0,0 to 127,63
#oled.rect(2, 2, 126, 62, 1)        # draw a rectangle outline 10,10 to 117,53, colour=1
#oled.fill_rect(10, 10, 107, 43, 1)   # draw a solid rectangle 10,10 to 117,53, colour=1

oled.show()