from machine import Pin, ADC, PWM
from time import sleep

led_pwm = PWM(Pin(0), 10000)

#Configure ADC for ESP32
pot = ADC(Pin(34))
pot.width(ADC.WIDTH_10BIT)
pot.atten(ADC.ATTN_11DB)

while True:
	pot_value = pot.read()
	print(f'status pot: {pot_value}')
	percent_pot_value = int((100*pot_value)/1023)
	print(f'status percent_pot_value: {percent_pot_value}')
	led_pwm.duty(pot_value)
	sleep(0.1)