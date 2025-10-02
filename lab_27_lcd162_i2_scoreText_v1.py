#lab_27_lcd162_i2_scoreText_v1.py
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

def scroll_message(message, delay=0.1):
    # Add spaces to the beginning of the message to make it appear from the right
    message = " " * I2C_NUM_COLS + message + " "
    # Scroll through the message
    for i in range(len(message) - I2C_NUM_COLS + 1):
        lcd.move_to(0, 0)
        lcd.putstr(message[i:i + I2C_NUM_COLS])
        sleep(delay)

try:
	while True:
		lcd.clear() # เคลียร์หน้าจอ
		lcd.putstr("Scolling Text") #แสดงตัวอักษร
		sleep(2)
		message_scroll = "This is a scrolling message with more than 16 characters"
		scroll_message(message_scroll)

except KeyboardInterrupt:
	# Turn off the display
	print("Keyboard interrupt")
	lcd.backlight_off()
	lcd.display_off()