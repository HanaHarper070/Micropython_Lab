#lab24_dht22_soilmc_oled.py
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
		
		# กรอบสี่เหลี่ยม
		oled.rect(2, 2, 126, 62, 1) 
		oled.rect(2, 2, 126, 20, 1)
		
		#weather today
		oled.text("Weather today", 12, 8)
		
		#Temperature
		oled.text("Temp: ", 10, 26)
		oled.text(temp_txt, 60, 26)
		oled.text("C", 110, 26)
		
		#Humidity
		oled.text("Humi: ", 10, 39)
		oled.text(hum_txt, 60, 39)
		oled.text("%", 110, 39)
		
		#Soil MC
		oled.text("Soli: ", 10, 52)
		oled.text(str(80.00), 60, 52)
		oled.text("%", 110, 52)
		oled.show()
	except OSError as e:
		print('Failed to read sensor.')