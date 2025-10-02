#lab_24_lcd162_i2_2line_newlib.py

from machine import Pin, SoftI2C
from lcd1602_2004_i2c import LCD
from time import sleep

scl_pin = 22
sda_pin = 21
lcd = LCD(SoftI2C(scl=Pin(scl_pin), sda=Pin(sda_pin), freq=100000))

lcd.puts("Hello, Line 1!", 0, 0) #put("text", row, start index)
lcd.puts("Hello, Line 2!", 1, 0) #put("text", row, start index)
sleep(1) 
lcd.clear()

lcd.puts("Line 1!", 0, 1) #put("text", row, start index)
lcd.puts("Line 2!", 1, 3) #put("text", row, start index)
sleep(1) 
lcd.clear()

lcd.puts("Line 1!", 0, 2) #put("text", row, start index)
lcd.puts("Line 2!", 1, 5) #put("text", row, start index)
sleep(1) 
lcd.clear()