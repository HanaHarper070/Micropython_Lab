#lab_26_lcd162_i2_morethan2line.py
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


lcd.clear() # เคลียร์หน้าจอ

# Line 1 
lcd.move_to(0, 0) #คอลัมน์ที่ 0, แถวที่ 0 (ชิดซ้ายสุด, แถวที่ 1)
lcd.putstr("Welcome 2 ESP") #แสดงตัวอักษร
# Line 2
lcd.move_to(0, 1) #คอลัมน์ที่ 0, แถวที่ 1 (ชิดซ้ายสุด, แถวที่ 2)
lcd.putstr("Nice to meet U") #แสดงตัวอักษร
sleep(2)
lcd.clear() # เคลียร์หน้าจอ

# Line 1 
lcd.move_to(0, 0) #คอลัมน์ที่ 0, แถวที่ 0 (ชิดซ้ายสุด, แถวที่ 1)
lcd.putstr("5555") #แสดงตัวอักษร
# Line 2
lcd.move_to(5, 1) #คอลัมน์ที่ 0, แถวที่ 1 (ชิดซ้ายสุด, แถวที่ 2)
lcd.putstr("END") #แสดงตัวอักษร
sleep(2)
lcd.clear() # เคลียร์หน้าจอ