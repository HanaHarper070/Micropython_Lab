from machine import Pin, ADC, PWM
from time import sleep


led_red = Pin(0, Pin.OUT)
led_green = Pin(4, Pin.OUT)
led_yellow = Pin(16, Pin.OUT)

#Configure ADC for ESP32
soil = ADC(Pin(35))
soil.width(ADC.WIDTH_10BIT)
soil.atten(ADC.ATTN_11DB)

###########
soil_value_max = 639
soil_value_min = 195
###########

while True:
	soil_value = soil.read()
	print(f'status soil: {soil_value}')
	percent_soil_value = int((soil_value_max-soil_value)*100/(soil_value_max-soil_value_min))
	print(f'status percent_soil_value: {percent_soil_value}')
	if percent_soil_value <= 35:
		led_red.on()
	elif percent_soil_value <= 50: 
		led_yellow.on()
	elif percent_soil_value >= 85: 
		led_green.on()
	else:
		led_green.off()
		led_red.off()
		led_yellow.off()
	sleep(0.1)