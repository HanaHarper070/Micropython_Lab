#lab_29_lcd162_i2c_scoll_dht22.py
from machine import Pin, SoftI2C
from machine_i2c_lcd import I2cLcd
from time import sleep
from dht import DHT22

# Define the LCD I2C address and dimensions
I2C_ADDR = 0x27
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16

# Initialize I2C and LCD objects
i2c = SoftI2C(sda=Pin(21), scl=Pin(22), freq=400000)

lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)

dht22 = DHT22(Pin(23))


def scroll_message_line1(message, delay=0.1):
    message = " " * I2C_NUM_COLS + message + " "
    for i in range(len(message) - I2C_NUM_COLS + 1):
        lcd.move_to(0, 0)
        lcd.putstr(message[i:i + I2C_NUM_COLS])
        sleep(delay)
        
def scroll_message_line2(message, delay=0.1):
    message = " " * I2C_NUM_COLS + message + " "
    for i in range(len(message) - I2C_NUM_COLS + 1):
        lcd.move_to(0, 1)
        lcd.putstr(message[i:i + I2C_NUM_COLS])
        sleep(delay)
        
lcd.clear() # เคลียร์หน้าจอ

try:
	while True:
		dht22.measure()
		temp = round(dht22.temperature(), 2)
		humi = round(dht22.humidity(), 2)

		temp = round(temp, 2)
		humi = round(humi, 2)

		temp_str = str(temp)
		humi_str = str(humi)
		sleep(0.5)

		# Line 1
		lcd.move_to(2, 0) #คอลัมน์ที่ 0, แถวที่ 0 (ชิดซ้ายสุด, แถวที่ 1)
		lcd.putstr("Weather Today") #แสดงตัวอักษร

		# Line 2 Score
		message_scroll_line2 = f"Temperature: {temp_str} °C & Humidity: {humi_str} %"
		scroll_message_line2(message_scroll_line2)

except KeyboardInterrupt:
	# Turn off the display
	print("Keyboard interrupt")
	lcd.backlight_off()
	lcd.display_off()
