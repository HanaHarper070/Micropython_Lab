#lab23_dht22_oled.py
from machine import Pin, SoftI2C
import ssd1306
from time import sleep
import dht 

# ESP32 Pin assignment 
#DHT22
dht22 = dht.DHT22(Pin(14))
#OLED_I2C
#i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
i2c = SoftI2C(scl=Pin(5), sda=Pin(4))
oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

while True:
	try:
		sleep(2)
		dht22.measure()
		temp = round(dht22.temperature(),2 )
		hum = round(dht22.humidity(),2 )
		print('Temperature: %3.1f C' %temp)
		print('Humidity: %3.1f %%' %hum)
		
		oled.fill(0)
		temp_txt = str(temp)
		hum_txt = str(hum)
		oled.text(temp_txt, 5, 10)
		oled.text(hum_txt, 5, 30)
		oled.show()
	except OSError as e:
		print('Failed to read sensor.')
