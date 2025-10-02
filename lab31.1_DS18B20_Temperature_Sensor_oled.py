#lab26_DS18B20_Temperature_Sensor_oled.py
import time
from onewire import OneWire
from ds18x20 import DS18X20
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

ds18b20_pin = Pin(27)
ds18b20_sensor = DS18X20(OneWire(ds18b20_pin))
roms = ds18b20_sensor.scan() # scan for DS18B20 sensors. The addresses found are saved on the roms
print('Found DS devices: ', roms)

while True:
  try:
    sleep(2)
    sensor.measure()
    temp = round(sensor.temperature(), 2)
    hum = round(sensor.humidity(), 2)
    print('Temperature: %3.1f C' %temp)
    print('Humidity: %3.1f %%' %hum)
    
    ds18b20_sensor.convert_temp()
    time.sleep_ms(750)
    for rom in roms:
        print(rom)
        print(f' Temperature DS: {ds18b20_sensor.read_temp(rom)} C')

    print("* " * 25)
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
    
    oled.text(f"TempAir: {temp} C", 4, 25) # ("text", X, Y)
    oled.text(f"HumiAir: {hum} %", 4, 38) # ("text", X, Y)
    oled.text(f"TempDSB: {ds18b20_sensor.read_temp(rom)} C", 4, 51) # ("text", X, Y)
    
    oled.show()
  except OSError as e:
    print('Failed to read sensor.')