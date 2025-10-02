#lab_17_dht22.py
# 1. ดึงไลบรารี่ dht มาใช้
from machine import Pin
import dht

# 2. สร้างตัวแปรรับค่า dht 22 ที่ขาพินที่ 14
#dht11 = dht.DHT11(Pin(14))
dht22 = dht.DHT22(Pin(14))

# 3. อ่านค่า dht 22
dht22.measure() # เริ่มต้นการอ่านค่าเซนเซอร์ dht22
dht22.temperature() # เริ่มต้นการอ่านค่า อุณหภูมิ เซนเซอร์ dht22
dht22.humidity() # เริ่มต้นการอ่านค่า ความชื้น เซนเซอร์ dht22
print(dht22.temperature())
print(dht22.humidity())