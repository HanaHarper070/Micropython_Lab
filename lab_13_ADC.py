from machine import Pin, ADC
from time import sleep

#Configure ADC for ESP32
pot = ADC(Pin(34))
pot.width(ADC.WIDTH_10BIT)
pot.atten(ADC.ATTN_11DB)

while True:
	pot_value = pot.read()
	print(f'status pot: {pot_value}')
	percent_pot_value = int((100*pot_value)/1023)
	print(f'status percent_pot_value: {percent_pot_value}')
	sleep(0.1)