#env_sensors_module.py
# env_sensors.py
# Unified sensor reader for ESP32/ESP32-S3
# Supports: DS18B20, BH1750, DHT22, Soil Moisture (ADC)
from machine import Pin, SoftI2C, ADC
from ds18x20 import DS18X20
from onewire import OneWire
from bh1750 import BH1750
import dht
from time import sleep

def _clamp(v, lo, hi):
    return lo if v < lo else hi if v > hi else v

class EnvSensors:
    def __init__(
        self,
        # I2C (BH1750)
        i2c_scl: int = 22,
        i2c_sda: int = 21,
        i2c_freq: int = 400_000,
        bh1750_addr: int = 0x23,
        # DHT22
        dht_pin: int = 14,
        # DS18B20 (OneWire)
        ds18b20_pin: int = 4,
        # Soil moisture (ADC)
        soil_adc_pin: int = 34,
        soil_width: int = ADC.WIDTH_10BIT,
        soil_atten: int = ADC.ATTN_11DB,
        soil_min: int = 100,   # แห้งสุด (ค่า ADC ที่วัดได้)
        soil_max: int = 600,   # เปียกสุด (ค่า ADC ที่วัดได้)
    ):
        # --- I2C / BH1750 ---
        self.i2c = SoftI2C(scl=Pin(i2c_scl), sda=Pin(i2c_sda), freq=i2c_freq)
        self.light = BH1750(bus=self.i2c, addr=bh1750_addr)

        # --- DHT22 ---
        self.dht = dht.DHT22(Pin(dht_pin))

        # --- DS18B20 ---
        self.ds = DS18X20(OneWire(Pin(ds18b20_pin)))
        self.ds_roms = self.ds.scan() or []
        # หมายเหตุ: อาจมีหลายหัววัดบนบัสเดียวกัน

        # --- Soil Moisture (ADC) ---
        self.soil = ADC(Pin(soil_adc_pin))
        self.soil.width(soil_width)
        self.soil.atten(soil_atten)
        self.soil_min = int(soil_min)
        self.soil_max = int(soil_max)

    # ---------- Readers ----------
    def read_dht(self):
        """Return (temp_c, rh) หรือ (None, None) เมื่ออ่านไม่สำเร็จ"""
        try:
            self.dht.measure()
            t = self.dht.temperature()
            h = self.dht.humidity()
            return float(t), float(h)
        except Exception:
            return None, None

    def read_soil(self):
        """
        Return (raw, percent)
        - raw: ค่า ADC ตาม width/atten
        - percent: 0-100 (คำนวณจาก soil_min/soil_max)
        """
        raw = self.soil.read()
        # soil_max = เปียกสุด → 100%
        # soil_min = แห้งสุด → 0%
        try:
            pct = int((self.soil_max - raw) * 100 / (self.soil_max - self.soil_min))
        except ZeroDivisionError:
            pct = 0
        pct = _clamp(pct, 0, 100)
        return int(raw), int(pct)

    def read_bh1750(self):
        """Return lux (float) หรือ None"""
        try:
            lux = self.light.luminance(BH1750.CONT_HIRES_1)
            return float(lux)
        except Exception:
            return None

    def read_ds18b20(self, wait_ms: int = 750):
        """
        Return list ของอุณหภูมิ DS18B20 (°C) อาจว่างถ้าไม่เจอหัววัด
        """
        if not self.ds_roms:
            return []
        try:
            self.ds.convert_temp()
            sleep(wait_ms / 1000)
            temps = []
            for rom in self.ds_roms:
                t = self.ds.read_temp(rom)
                temps.append(round(float(t), 2))
            return temps
        except Exception:
            return []

    def read_all(self):
        """
        อ่านทุกตัวแล้วคืน dict รวมผลลัพธ์
        {
          'dht_temp_c': float|None,
          'dht_rh': float|None,
          'soil_raw': int,
          'soil_pct': int,
          'lux': float|None,
          'ds18b20_temps': list[float],
          'ds18b20_t_avg': float|None
        }
        """
        t_dht, rh = self.read_dht()
        soil_raw, soil_pct = self.read_soil()
        lux = self.read_bh1750()
        ds_temps = self.read_ds18b20()
        ds_avg = round(sum(ds_temps) / len(ds_temps), 2) if ds_temps else None

        return {
            'dht_temp_c': t_dht,
            'dht_rh': rh,
            'soil_raw': soil_raw,
            'soil_pct': soil_pct,
            'lux': None if lux is None else round(lux, 2),
            'ds18b20_temps': ds_temps,
            'ds18b20_t_avg': ds_avg,
        }

    # ---------- Utilities ----------
    def calibrate_soil(self, soil_min: int = None, soil_max: int = None):
        """อัปเดตค่าคาลิเบรตดินเปียก/แห้ง"""
        if soil_min is not None:
            self.soil_min = int(soil_min)
        if soil_max is not None:
            self.soil_max = int(soil_max)