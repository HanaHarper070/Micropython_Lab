from machine import Pin, ADC, PWM
from time import sleep

#led_pwm = PWM(Pin(0), 10000)

#Configure ADC for ESP32
soil = ADC(Pin(26))
#soil.width(ADC.WIDTH_10BIT)
#soil.atten(ADC.ATTN_11DB)

###########
soil_value_max = 639
soil_value_min = 195
###########

while True:
	soil_value = soil.read_u16()
	print(f'status soil: {soil_value}')
	percent_soil_value = int((soil_value_max-soil_value)*100/(soil_value_max-soil_value_min))
	print(f'status percent_soil_value: {percent_soil_value}')
	#led_pwm.duty(soil_value)
	sleep(0.1)