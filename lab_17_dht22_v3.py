#lab_17_dht22_v3.py
# 1. ดึงไลบรารี่ dht มาใช้
from machine import Pin # นำเข้าไลบรารี่ machine 
import dht # นำเข้าไลบรารี่ dht
import time # นำเข้าไลบรารี่ time

# 2. สร้างตัวแปรรับค่า dht 22 ที่ขาพินที่ 14
#dht11 = dht.DHT11(Pin(14))
dht22 = dht.DHT22(Pin(14))

# 3. อ่านค่า dht 22
while True:
	dht22.measure() # เริ่มต้นการอ่านค่าเซนเซอร์ dht22

	temp = dht22.temperature() # เริ่มต้นการอ่านค่า อุณหภูมิ เซนเซอร์ dht22
	humi = dht22.humidity() # เริ่มต้นการอ่านค่า ความชื้น เซนเซอร์ dht22

	temp = round(temp, 2) # คำสั่งให้มีทศนิยม 2 ตำแหน่ง
	humi = round(humi, 2) # คำสั่งให้มีทศนิยม 2 ตำแหน่ง

	print(f' Temperature: {temp} C') #แสดงผลบนหน้า shell
	print(f' Humidity: {humi} %') #แสดงผลบนหน้า shell
	print("* " * 25)
	time.sleep(2)