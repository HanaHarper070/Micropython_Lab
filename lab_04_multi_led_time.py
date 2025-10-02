# เรียกใช้โมดูล
from machine import Pin # เรียกโมดูล machine เรียกใช้ขา pin
from time import sleep # เรียกโมดูล time เรียกใช้ delay/หน่วงเวลา

# ประกาศตัวแปร
led_R = Pin(5, Pin.OUT) # สร้างตัวแปร led ใช้ขา 5 เป็นขาแสดงผลลัพธ์ (OUTPUT)
led_Y = Pin(17, Pin.OUT) # สร้างตัวแปร led ใช้ขา 17 เป็นขาแสดงผลลัพธ์ (OUTPUT)
led_G = Pin(16, Pin.OUT) # สร้างตัวแปร led ใช้ขา 16 เป็นขาแสดงผลลัพธ์ (OUTPUT)
print(f'Red led status: {led_R.value()}')
print(f'Yellow led status: {led_Y.value()}')
print(f'Green led status: {led_G.value()}')

while True: 
	led_R.on()
	sleep(0.5)
	led_R.off()
	sleep(0.5)
	
	led_Y.on()
	sleep(0.5)
	led_Y.off()
	sleep(0.5)
	
	led_R.on()
	sleep(0.5)
	led_R.off()
	sleep(0.5)

	led_G.on()
	sleep(0.5)
	led_G.off()
	sleep(0.5)
