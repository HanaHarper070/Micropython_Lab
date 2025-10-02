# env_sensors_portable.py
# Cross-board sensor reader for ESP32/ESP32-S3/ESP32-C3 and Raspberry Pi Pico/Pico W
# DHT22 (temp, RH) + BH1750 (lux) + DS18B20 (temps[]) + Soil moisture (ADC)
# - Auto pin defaults by board, overridable via ctor
# - HW I2C if possible -> fallback to SoftI2C
# - Safe when some sensors are missing (returns None/[] instead of crashing)

from machine import Pin, I2C, SoftI2C, ADC
import sys
from time import sleep

# Optional imports (graceful if driver is absent)
try:
    import dht
except Exception:
    dht = None

try:
    from ds18x20 import DS18X20
    from onewire import OneWire
except Exception:
    DS18X20 = None
    OneWire = None

try:
    from bh1750 import BH1750
except Exception:
    BH1750 = None

# ---------------- Utils ----------------
def _clamp(v, lo, hi):
    return lo if v < lo else hi if v > hi else v

def _supports(obj, name):
    return hasattr(obj, name)

def _is_rp2():
    return sys.platform.startswith("rp2")

def _is_esp32():
    # บน MicroPython ตระกูล ESP32 (รวม C3/S3) จะได้ 'esp32'
    return sys.platform.startswith("esp32")

# ---------------- Pin profiles ----------------
# ดีฟอลต์ที่ใช้งานได้ทั่วไป (แก้ได้ตามบอร์ดของคุณ)
# หมายเหตุ: บอร์ด ESP32 ต่างยี่ห้ออาจวาง I/O ไม่เหมือนกัน
BOARD_PROFILES = {
    # Raspberry Pi Pico / Pico W (RP2040)
    "rp2": dict(
        i2c_id=0, i2c_scl=5, i2c_sda=4, i2c_freq=100_000,
        dht_pin=16,            # ใช้ GPIO ดิจิทัลอิสระ
        ds_pin=15,             # ต้องมี R 4.7k ระหว่าง DATA->3V3
        soil_adc_pin=26,       # ADC0 = GP26
        soil_width=None, soil_atten=None,
    ),
    # ESP32 / ESP32-S3 / ESP32-C3 (ปรับตามบอร์ดคุณได้)
    "esp32": dict(
        i2c_id=0, i2c_scl=22, i2c_sda=21, i2c_freq=100_000,
        dht_pin=14,
        ds_pin=4,              # นิยมใช้ GPIO4 เป็น 1-Wire
        soil_adc_pin=34,       # ADC1 channel (input only)
        # กรณีต้องการ ระบุ width/atten (ถ้าบอร์ดรองรับ)
        soil_width=None,       # e.g. ADC.WIDTH_12BIT
        soil_atten=None,       # e.g. ADC.ATTN_11DB
    ),
}

# ---------------- Main class ----------------
class EnvSensors:
    def __init__(
        self,
        # เลือก profile อัตโนมัติตามบอร์ด (rp2/esp32) หรือใส่เอง: "rp2" / "esp32"
        profile: str = None,

        # I2C (BH1750)
        use_soft_i2c: bool = False,
        i2c_id: int = None,
        i2c_scl: int = None,
        i2c_sda: int = None,
        i2c_freq: int = None,
        bh1750_addr: int = 0x23,

        # DHT22
        dht_pin: int = None,

        # DS18B20 (OneWire)
        ds18b20_pin: int = None,

        # Soil Moisture (ADC)
        soil_adc_pin: int = None,
        soil_width=None,     # ESP32-only
        soil_atten=None,     # ESP32-only
        soil_min: int = 100, # แห้งสุด (raw)
        soil_max: int = 600, # เปียกสุด (raw)
    ):
        # --- resolve profile ---
        if profile is None:
            profile = "rp2" if _is_rp2() else "esp32" if _is_esp32() else "esp32"
        self.platform = profile

        # default pins by profile
        p = BOARD_PROFILES.get(profile, BOARD_PROFILES["esp32"]).copy()

        # override from args (if provided)
        if i2c_id is not None:   p["i2c_id"] = i2c_id
        if i2c_scl is not None:  p["i2c_scl"] = i2c_scl
        if i2c_sda is not None:  p["i2c_sda"] = i2c_sda
        if i2c_freq is not None: p["i2c_freq"] = i2c_freq
        if dht_pin is not None:  p["dht_pin"] = dht_pin
        if ds18b20_pin is not None: p["ds_pin"] = ds18b20_pin
        if soil_adc_pin is not None: p["soil_adc_pin"] = soil_adc_pin
        if soil_width is not None:   p["soil_width"] = soil_width
        if soil_atten is not None:   p["soil_atten"] = soil_atten

        self.cfg = p
        self.soil_min = int(soil_min)
        self.soil_max = int(soil_max)

        # --- I2C (prefer HW, fallback Soft) ---
        self.i2c = None
        i2c_err = None
        if not use_soft_i2c:
            try:
                self.i2c = I2C(
                    p["i2c_id"],
                    scl=Pin(p["i2c_scl"]),
                    sda=Pin(p["i2c_sda"]),
                    freq=p["i2c_freq"],
                )
            except Exception as e:
                i2c_err = e
        if self.i2c is None:
            try:
                self.i2c = SoftI2C(
                    scl=Pin(p["i2c_scl"]),
                    sda=Pin(p["i2c_sda"]),
                    freq=p["i2c_freq"],
                )
            except Exception as e:
                raise RuntimeError("I2C init failed (HW:%s / Soft:%s)" % (i2c_err, e))

        # --- BH1750 (optional) ---
        self.light = None
        if BH1750 is not None:
            try:
                self.light = BH1750(bus=self.i2c, addr=bh1750_addr)
            except Exception:
                self.light = None  # ไม่มี/ต่อไม่ถูก จะปล่อย None

        # --- DHT22 (optional) ---
        self.dht = None
        if dht is not None:
            try:
                self.dht = dht.DHT22(Pin(p["dht_pin"]))
            except Exception:
                self.dht = None

        # --- DS18B20 (optional) ---
        self.ds = None
        self.ds_roms = []
        if DS18X20 is not None and OneWire is not None:
            try:
                self.ds = DS18X20(OneWire(Pin(p["ds_pin"])))
                self.ds_roms = self.ds.scan() or []
            except Exception:
                self.ds = None
                self.ds_roms = []

        # --- Soil Moisture (ADC) ---
        self.soil = ADC(Pin(p["soil_adc_pin"]))
        # ESP32 เท่านั้นที่มี width/atten
        if p["soil_width"] is not None and _supports(self.soil, "width"):
            try:
                self.soil.width(p["soil_width"])
            except Exception:
                pass
        if p["soil_atten"] is not None and _supports(self.soil, "atten"):
            try:
                self.soil.atten(p["soil_atten"])
            except Exception:
                pass

    # ---------------- Readers ----------------
    def read_dht(self):
        """Return (temp_c, rh) หรือ (None, None) หากไม่มี DHT/อ่านไม่สำเร็จ"""
        if self.dht is None:
            return None, None
        try:
            self.dht.measure()
            t = self.dht.temperature()
            h = self.dht.humidity()
            return float(t), float(h)
        except Exception:
            return None, None

    def _adc_read_any(self):
        """
        ESP32: อาจมี read()  (0..4095 / แล้วแต่ width)
        RP2040: ใช้ read_u16() (0..65535)
        """
        if _supports(self.soil, "read_u16"):
            return self.soil.read_u16()
        elif _supports(self.soil, "read"):
            return self.soil.read()
        else:
            try:
                return int(self.soil.read_u16())
            except Exception:
                return 0

    def read_soil(self):
        """
        Return (raw, percent)
        - raw: ค่า ADC raw
        - percent: 0-100 คิดจาก (soil_min, soil_max) ที่คาลิเบรตไว้
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
        if self.light is None:
            return None
        try:
            # ใช้โหมดต่อเนื่องความละเอียดสูง
            return float(self.light.luminance(BH1750.CONT_HIRES_1))
        except Exception:
            return None

    def read_ds18b20(self, wait_ms: int = 750):
        """
        Return list อุณหภูมิ DS18B20 (°C); [] หากไม่มีหัววัด/อ่านไม่ได้
        """
        if not self.ds_roms or self.ds is None:
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
        อ่านทุกตัวแล้วคืน dict:
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

    # ---------------- Helpers ----------------
    def calibrate_soil(self, soil_min: int = None, soil_max: int = None):
        """อัปเดตการคาลิเบรตดิน (อิง raw) — ทำบนบอร์ดเดียวกับที่จะใช้งานจริง"""
        if soil_min is not None:
            self.soil_min = int(soil_min)
        if soil_max is not None:
            self.soil_max = int(soil_max)

    def pretty(self, data: dict) -> str:
        """แปลง dict เป็นข้อความอ่านง่าย"""
        lines = []
        for k in ("dht_temp_c","dht_rh","soil_raw","soil_pct","lux","ds18b20_t_avg"):
            lines.append(f"{k}: {data.get(k)}")
        if "ds18b20_temps" in data:
            lines.append(f"ds18b20_temps: {data['ds18b20_temps']}")
        return "\n".join(lines)

    def to_json(self, data: dict) -> str:
        """แปลง dict เป็น JSON แบบ lightweight (ไม่ต้อง import ujson)"""
        def _v(v):
            if v is None:
                return "null"
            if isinstance(v, (int, float)):
                return str(v)
            if isinstance(v, list):
                return "[" + ",".join(_v(x) for x in v) + "]"
            # string
            s = str(v).replace('"', '\\"')
            return f"\"{s}\""
        items = []
        for k, v in data.items():
            items.append(f"\"{k}\":{_v(v)}")
        return "{" + ",".join(items) + "}"