#labxx_data2gsheet.py
from machine import Pin, ADC, I2C, SoftI2C
import urequests
import data2gsheet
import gc
import network
import time
import random

# ปิด debug ของ ESP (ถ้าใช้ ESP8266/ESP32)
try:
    import esp
    esp.osdebug(None)
except:
    pass

gc.collect()

############# WiFi Config #################
def wifi_connect():
    ssid = 'Hana_Harpel22.4G'
    password = 'hanaharper2513'
    station = network.WLAN(network.STA_IF)
    station.active(True)
    if not station.isconnected():
        print('Connecting to WiFi...')
        station.connect(ssid, password)
        while not station.isconnected():
            pass
    print('WiFi connected:', station.ifconfig())
############# WiFi Config #################

######## Google Apps Script ID #############
GAS_ID = "AKfycbyu1NkECJ11LjIYtgGtYRy5-qu2kIiK7ilW_unpTygZb-3o8EfG2IECpJco4Wp0AI3v"  # Google Script id from deploy app >>> Deployment ID:
######## Google Apps Script ID #############

###########  Function to send data to Google Sheet ################
def send_data_to_ggsheet(temp, humi, light, soilmc):
	global GAS_ID
	print(("Temperature: {} °C, Humidity: {} %RH, Light: {} lux, SoilMC: {} %\n".format(temp, humi, light, soilmc)))
	url = "https://script.google.com/macros/s/" + GAS_ID + "/exec?"
	data = "temp=" + str(temp) + "&humi=" + str(humi) + "&light=" + str(light) + "&soilmc=" + str(soilmc)
	url_data = url + data
	print("Posting Temperature, Humidity, Light Intensity and soil MC data to Google Sheet")

	try:
		response = urequests.get(url_data)
		print("HTTP Status Code:", response.status_code)
		payload = response.text
		print("Payload:", payload)
		print("Temperature: %d°C, Humidity: %d%%, Light: %d lux, SoilMC: %d%%" % (temp, humi, light, soilmc))
		response.close()
		gc.collect()
	except Exception as err:
		print(f"Error occurred: {err}")

###########  Function to send data to Google Sheet ################

############# เริ่มต้นระบบ #################
wifi_connect()

last_message = 0
message_interval = 60 # 600 sec = 10 min

while True:
	try:
		current_time = time.time()
		if current_time - last_message > message_interval:
			humidity = random.randint(0, 95)
			light = random.randint(0, 62000)
			temperature= random.randint(25, 45)
			soilmc = random.randint(15, 95)

			#data2gsheet
			print("Sending data to gsheet...")
			send_data_to_ggsheet(temperature, humidity, light, soilmc)
			print("Data sent to gsheet successfully\n------------------------")
			last_message = current_time
			gc.collect()
	except OSError as e:
		print("Loop error:", e)