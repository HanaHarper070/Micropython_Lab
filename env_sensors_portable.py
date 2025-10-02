# env_sensors_portable.py
# Cross-board sensor reader for ESP32/ESP32-S3 and Raspberry Pi Pico/Pico W
from machine import Pin, I2C, SoftI2C, ADC
from ds18x20 import DS18X20
from onewire import OneWire
from bh1750 import BH1750
import dht
import sys
from time import sleep

def _clamp(v, lo, hi):
    return lo if v < lo else hi if v > hi else v

def _supports(obj, name):
    return hasattr(obj, name)

class EnvSensors:
    def __init__(
        self,
        # --- I2C (BH1750) ---
        use_soft_i2c: bool = False,    # Pico/ESP ใช้ hw I2C จะนิ่งกว่า; ตั้ง True หากอยากใช้ SoftI2C
        i2c_id: int = 0,               # ใช้เมื่อเป็นฮาร์ดแวร์ I2C
        i2c_scl: int = 5,              # DEFAULT สำหรับ Pico W (I2C0 SCL=GP5)
        i2c_sda: int = 4,              # DEFAULT สำหรับ Pico W (I2C0 SDA=GP4)
        i2c_freq: int = 100_000,
        bh1750_addr: int = 0x23,

        # --- DHT22 ---
        dht_pin: int = 16,             # DEFAULT ตัวอย่างสำหรับ Pico W (เลือก GPIO ดิจิทัลใดก็ได้)

        # --- DS18B20 (OneWire) ---
        ds18b20_pin: int = 15,         # DEFAULT ตัวอย่างสำหรับ Pico W
                                       # (อย่าลืมตัวต้านทาน 4.7k ระหว่าง DATA->3V3)

        # --- Soil Moisture (ADC) ---
        soil_adc_pin: int = 26,        # DEFAULT: Pico W ADC0 = GP26
        # ESP-specific (จะ try/except ให้):
        soil_width=None,               # e.g., ADC.WIDTH_10BIT (ESP-only)
        soil_atten=None,               # e.g., ADC.ATTN_11DB  (ESP-only)
        soil_min: int = 100,           # แห้งสุด (ค่า ADC ที่วัดได้)
        soil_max: int = 600,           # เปียกสุด (ค่า ADC ที่วัดได้)

    ):
        # --- I2C / BH1750 ---
        if use_soft_i2c:
            self.i2c = SoftI2C(scl=Pin(i2c_scl), sda=Pin(i2c_sda), freq=i2c_freq)
        else:
            # ใช้ฮาร์ดแวร์ I2C; บน Pico W: i2c_id=0, scl=GP5, sda=GP4
            self.i2c = I2C(i2c_id, scl=Pin(i2c_scl), sda=Pin(i2c_sda), freq=i2c_freq)

        self.light = BH1750(bus=self.i2c, addr=bh1750_addr)

        # --- DHT22 ---
        self.dht = dht.DHT22(Pin(dht_pin))

        # --- DS18B20 ---
        self.ds = DS18X20(OneWire(Pin(ds18b20_pin)))
        self.ds_roms = self.ds.scan() or []

        # --- Soil Moisture (ADC) ---
        self.soil = ADC(Pin(soil_adc_pin))
        # เฉพาะ ESP จะมี width/atten; Pico ไม่มีเมธอดนี้
        if soil_width is not None and _supports(self.soil, "width"):
            try:
                self.soil.width(soil_width)
            except Exception:
                pass
        if soil_atten is not None and _supports(self.soil, "atten"):
            try:
                self.soil.atten(soil_atten)
            except Exception:
                pass

        self.soil_min = int(soil_min)
        self.soil_max = int(soil_max)

        # ตรวจว่ากำลังรันบน Pico/ESP (เผื่ออยากใช้ต่อในภายหลัง)
        self.platform = sys.platform  # 'rp2' สำหรับ Pico/Pico W, 'esp32' สำหรับ ESP32/-S3

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

    def _adc_read_any(self):
        """
        บน ESP32: มี read() (0..4095/1023 แล้วแต่ width)
        บน Pico:   ไม่มี read() แต่มี read_u16() (0..65535)
        """
        if _supports(self.soil, "read_u16"):
            return self.soil.read_u16()
        elif _supports(self.soil, "read"):
            return self.soil.read()
        else:
            # fallback
            try:
                return int(self.soil.read_u16())
            except Exception:
                return 0

    def read_soil(self):
        """
        Return (raw, percent)
        - raw: ค่า ADC raw (สเกลขึ้นกับบอร์ด)
        - percent: 0-100 คำนวณเทียบกับ soil_min/soil_max ที่ผู้ใช้กำหนดเอง (อิง raw)
        หมายเหตุ: ควรคาลิเบรต soil_min/soil_max บน "บอร์ดนั้น ๆ" เพราะสเกลต่างกัน
        """
        raw = self._adc_read_any()
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
        """อัปเดตค่าคาลิเบรตดินเปียก/แห้ง (อิง raw ของบอร์ดนั้น ๆ)"""
        if soil_min is not None:
            self.soil_min = int(soil_min)
        if soil_max is not None:
            self.soil_max = int(soil_max)