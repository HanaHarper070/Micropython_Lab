#lab_23_lcd162_i2_1line.py
from machine import Pin, SoftI2C
from machine_i2c_lcd import I2cLcd
from time import sleep

# Define the LCD I2C address and dimensions
I2C_ADDR = 0x27
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16

# Initialize I2C and LCD objects
i2c = SoftI2C(sda=Pin(21), scl=Pin(22), freq=400000)

lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)

# 1 Line
lcd.clear() # เคลียร์หน้าจอ
lcd.putstr("It's work line1") #แสดงตัวอักษร
sleep(1)

lcd.clear() # เคลียร์หน้าจอ
lcd.putstr("LCD 16*2 line1") #แสดงตัวอักษร
sleep(1)

lcd.clear()