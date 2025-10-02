#lab_24_lcd162_i2_2line_newlib_v2.py

from machine import I2C, Pin
from lcd1602 import LCD
import time

# Initialize I2C communication;
# Set SDA to pin 20, SCL to pin 21, and frequency to 400kHz
i2c = I2C(0, sda=Pin(21), scl=Pin(22), freq=400000)

# Create an LCD object for interfacing with the LCD1602 display
lcd = LCD(i2c)

# Display the first message on the LCD
# Use '\n' to create a new line.
string = "Line1\nLine2"
lcd.message(string)
# Wait for 2 seconds
time.sleep(2)
# Clear the display before exiting
lcd.clear()

string = "SunFounder\n LCD Tutorial"
lcd.message(string)
# Wait for 3 seconds
time.sleep(3)
# Clear the display
lcd.clear()

# Display the second message on the LCD
string = "Hello\n   World!"
lcd.message(string)
# Wait for 5 seconds
time.sleep(5)
# Clear the display before exiting
lcd.clear()