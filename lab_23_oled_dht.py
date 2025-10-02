#lab_23_oled_dht.py
from machine import Pin, SoftI2C
import ssd1306
from time import sleep
import dht 

sensor = dht.DHT22(Pin(14))
i2c = SoftI2C(scl=Pin(5), sda=Pin(4))
#i2c = SoftI2C(scl=Pin(22), sda=Pin(21))

oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

while True:
  try:
    sleep(2)
    sensor.measure()
    temp = round(sensor.temperature(), 2)
    hum = round(sensor.humidity(), 2)
    print('Temperature: %3.1f C' %temp)
    print('Humidity: %3.1f %%' %hum)
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
    oled.text(f"Temp: {temp} C", 8, 30) # ("text", X, Y)
    oled.text(f"Humi: {hum} %", 8, 45) # ("text", X, Y)
    oled.show()
  except OSError as e:
    print('Failed to read sensor.')