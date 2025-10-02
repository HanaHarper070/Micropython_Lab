#lab_24_oled_dht_soil.py
from machine import Pin, SoftI2C, ADC, PWM
import ssd1306
from time import sleep
import dht 

sensor = dht.DHT22(Pin(14))
i2c = SoftI2C(scl=Pin(5), sda=Pin(4))
#i2c = SoftI2C(scl=Pin(22), sda=Pin(21))

oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

led_pwm = PWM(Pin(0), 10000)

#Configure ADC for ESP32
soil = ADC(Pin(35))
soil.width(ADC.WIDTH_10BIT)
soil.atten(ADC.ATTN_11DB)

###########
soil_value_max = 639
soil_value_min = 195
###########

while True:
  try:
    sleep(2)
    sensor.measure()
    temp = round(sensor.temperature(), 2)
    hum = round(sensor.humidity(), 2)
    print('Temperature: %3.1f C' %temp)
    print('Humidity: %3.1f %%' %hum)
    
    soil_value = soil.read()
    print(f'status soil: {soil_value}')
    percent_soil_value = int((soil_value_max-soil_value)*100/(soil_value_max-soil_value_min))
    print(f'status percent_soil_value: {percent_soil_value}')
    percent_soil_value = round(percent_soil_value, 2)
    sleep(0.1)
    #percent_soil_value =  80.25
    
    print("* " * 20)
    #Text
    oled.fill(0)
    #text
    oled.text("Weather Today", 12, 7) # ("text", X, Y)
    # Hline
    oled.hline(1, 1, 127, 2) # (x, y, ยาว, หนา)
    oled.hline(1, 20, 127, 2) # (x, y, ยาว, หนา)
    oled.hline(1, 63, 127, 2) # (x, y, ยาว, หนา)
    # Vline
    oled.vline(1, 1, 63, 2) # (x, y, ยาว, หนา)
    oled.vline(127, 1, 63, 2) # (x, y, ยาว, หนา)
    oled.show()
    oled.text(f"Temp: {temp} C", 8, 25) # ("text", X, Y)
    oled.text(f"Humi: {hum} %", 8, 38) # ("text", X, Y)
    oled.text(f"Soil: {percent_soil_value} %", 8, 51) # ("text", X, Y)
    
    oled.show()
  except OSError as e:
    print('Failed to read sensor.')