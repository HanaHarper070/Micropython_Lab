#lab33_bh1750_v1.py
from machine import Pin, SoftI2C
from bh1750 import BH1750
import time

# Initialize I2C communication (ESP32)
i2c = SoftI2C(scl=Pin(5), sda=Pin(4))
#i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=400000)

# Create BH1750 object
light_sensor = BH1750(bus=i2c, addr=0x23)

while True:
	lux = light_sensor.luminance(BH1750.CONT_HIRES_1)
	print(f"Light Luminance: {lux} lux")
	time.sleep(2)