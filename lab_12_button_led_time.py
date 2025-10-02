from machine import Pin
from time import sleep

button_01 = Pin(34, Pin.IN)
led_onboard = Pin(2, Pin.OUT)
led_red = Pin(4, Pin.OUT)

toggle = 1

while True:
	status = button_01.value()
	print(f'button_01 status: {status}')
	if status == 1:
		if toggle == 1:
			led_onboard.value(1)
			led_red.on()
			toggle = 0
		else:
			led_onboard.value(0)
			led_red.off()
			toggle = 1
		sleep(0.1)