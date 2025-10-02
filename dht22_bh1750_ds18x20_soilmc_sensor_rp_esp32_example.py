from env_sensors_portable_v1 import EnvSensors
import time

PINS = {
    "i2c_scl": 5,       # BH1750 -> SCL (พบใช้บ่อยบน C3 devkit)
    "i2c_sda": 4,       # BH1750 -> SDA
    "dht_pin": 14,       # DHT22 data (ตัวอย่าง)
    "ds18b20_pin": 27,   # DS18B20 data
    "soil_adc_pin": 26   # เลือกขาที่เป็น ADC ได้จริงบนบอร์ดคุณ
}

sensor = EnvSensors(
    profile="rp2", #profile="esp32",
    i2c_id=0, i2c_scl=PINS["i2c_scl"], i2c_sda=PINS["i2c_sda"], i2c_freq=100_000,
    dht_pin=PINS["dht_pin"],
    ds18b20_pin=PINS["ds18b20_pin"],
    soil_adc_pin=PINS["soil_adc_pin"],
    # ถ้าบอร์ดรองรับ atten/width และต้องการกำหนด:
    # soil_width=ADC.WIDTH_12BIT, soil_atten=ADC.ATTN_11DB,
)

# (ทางเลือก) คาลิเบรต
# sensor.calibrate_soil(soil_min=120, soil_max=2200)
while  True:
	data = sensor.read_all()
	print(sensor.pretty(data))
	print(sensor.to_json(data))
	print("* " *25)
	time.sleep(2)