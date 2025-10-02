# main.py — ESP32 MicroPython: DHT22 + DS18B20 + OLED + Web Server (Pastel)
# ใช้กับบอร์ด ESP32 (รองรับ ESP8266 ได้ โดยปรับขา I2C/OneWire ให้เหมาะสม)
import network, socket, time
from machine import Pin, SoftI2C
from onewire import OneWire
from ds18x20 import DS18X20
import dht

# ----- (ถ้ามีจอ OLED) -----
try:
    import ssd1306
    HAS_OLED = True
except:
    HAS_OLED = False

# ===== 1) CONFIG =====

WIFI_SSID = "FM_IoT"
WIFI_PASS = "fm1234567890"
'''
WIFI_SSID = "Hana_Harpel22.4G"
WIFI_PASS = "hanaharper2513"
'''
# เลือกขาตามบอร์ด (ค่าด้านล่างสอดคล้องกับไฟล์เดิมของคุณ)
DHT_PIN = 14           # DHT22 -> Pin(14)
DS_PIN  = 27           # DS18B20 -> Pin(27)
I2C_SCL = 22           # OLED I2C SCL
I2C_SDA = 21           # OLED I2C SDA

# ===== 2) INIT SENSORS =====
sensor_dht = dht.DHT22(Pin(DHT_PIN))
ow = OneWire(Pin(DS_PIN))
ds = DS18X20(ow)
roms = ds.scan()  # ถ้ามีหลายตัวจะอ่านตัวแรก
print("Found DS devices:", roms)

oled = None
if HAS_OLED:
    try:
        i2c = SoftI2C(scl=Pin(I2C_SCL), sda=Pin(I2C_SDA), freq=400000)
        oled = ssd1306.SSD1306_I2C(128, 64, i2c)
    except Exception as e:
        print("OLED init error:", e)
        HAS_OLED = False

def oled_show(temp, hum, ds_temp):
    if not HAS_OLED or oled is None:
        return
    oled.fill(0)
    # กรอบและหัวข้อ (คล้ายไฟล์เดิม)
    oled.text("Weather Today", 8, 4)
    # เส้นกรอบ
    for x in [0, 127]:
        pass
    oled.hline(0, 0, 128, 1)
    oled.hline(0, 16, 128, 1)
    oled.hline(0, 63, 128, 1)
    oled.vline(0, 0, 64, 1)
    oled.vline(127, 0, 64, 1)
    # เนื้อหา
    oled.text("TempAir: {} C".format(temp if temp is not None else "-"), 4, 24)
    oled.text("HumiAir: {} %".format(hum if hum is not None else "-"), 4, 36)
    oled.text("TempDS : {} C".format(ds_temp if ds_temp is not None else "-"), 4, 48)
    oled.show()

# ===== 3) SENSOR READ =====
def read_sensors():
    """อ่าน DHT22 และ DS18B20 แล้วคืนค่า (temp, hum, ds_temp)"""
    t = h = td = None
    try:
        sensor_dht.measure()
        t = round(sensor_dht.temperature(), 2)
        h = round(sensor_dht.humidity(), 2)
    except Exception as e:
        print("DHT read error:", e)

    try:
        if roms:
            ds.convert_temp()
            time.sleep_ms(750)
            # อ่านตัวแรก (ถ้ามีหลายตัวสามารถวนลูปได้)
            td = ds.read_temp(roms[0])
            if td is not None:
                td = round(td, 2)
    except Exception as e:
        print("DS18B20 read error:", e)

    return t, h, td

# ===== 4) WIFI =====
def wifi_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connecting WiFi...")
        wlan.connect(WIFI_SSID, WIFI_PASS)
        timeout = 20
        while not wlan.isconnected() and timeout > 0:
            time.sleep(1)
            timeout -= 1
    if wlan.isconnected():
        print("WiFi connected:", wlan.ifconfig())
    else:
        print("WiFi connect failed")
    return wlan

# ===== 5) HTML (Pastel) =====
def pastel_html(temp, hum, ds_temp):
    # ดึงเวลา (tuple) จาก time.localtime()
    now = time.localtime()
    # จัดเป็น string เอง
    timestamp = "%04d-%02d-%02d %02d:%02d:%02d" % (
        now[0], now[1], now[2], now[3], now[4], now[5]
    )
    # ธีมพาสเทลแบบการ์ด — เบา ไม่ใช้ไฟล์ภายนอก
    return """<!DOCTYPE html>
<html lang="th">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>ESP Sensor Dashboard • Pastel</title>
<style>
:root{
  --bg1:#f8fbff; --bg2:#fff7fb; --txt:#334155; --muted:#64748b;
  --accent:#a78bfa; --accent2:#60a5fa; --accent3:#f472b6;
  --ring:#c7d2fe; --shadow:0 10px 30px rgba(31,41,55,.08); --r:22px;
}
*{box-sizing:border-box} html,body{margin:0;height:100%%;color:var(--txt);
  font-family: system-ui, -apple-system, Segoe UI, Roboto, 'Sarabun', Arial, sans-serif;
  background: radial-gradient(1200px 600px at 10%% 5%%, var(--bg2), transparent),
              radial-gradient(900px 500px at 90%% 10%%, #eef2ff, transparent),
              linear-gradient(180deg, #fbfeff, #fff);
}
.wrap{max-width:960px;margin:28px auto 48px;padding:0 16px}
header{display:flex;align-items:center;justify-content:center;gap:12px}
.logo{width:44px;height:44px;border-radius:14px;display:grid;place-items:center;
  background:linear-gradient(135deg,var(--accent),var(--accent2));color:#fff;box-shadow:var(--shadow)}
h1{margin:0;font-size:24px} .subtitle{color:var(--muted);font-size:13px;text-align:center;margin-top:4px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:16px;margin-top:18px}
.card{position:relative;background:linear-gradient(180deg,rgba(255,255,255,.75),rgba(255,255,255,.92));
  border:1px solid rgba(99,102,241,.12);border-radius:var(--r);padding:18px;box-shadow:var(--shadow);
  backdrop-filter:saturate(150%%) blur(6px);transition:.25s}
.card:hover{transform:translateY(-2px);box-shadow:0 14px 34px rgba(31,41,55,.10);border-color:var(--ring)}
.icon{width:42px;height:42px;border-radius:12px;display:grid;place-items:center;margin-bottom:8px;color:#fff}
.temp{background:linear-gradient(135deg,var(--accent2),#a7f3d0)}
.hum{ background:linear-gradient(135deg,#6ee7b7,var(--accent))}
.ds { background:linear-gradient(135deg,var(--accent3),var(--accent))}
.label{font-size:13px;color:var(--muted)} .value{display:flex;align-items:baseline;gap:6px;margin-top:4px}
.num{font-size:34px;font-weight:700} .unit{font-size:14px;color:var(--muted)}
footer{text-align:center;color:var(--muted);font-size:12px;margin-top:24px}
.chip{display:inline-flex;gap:8px;padding:6px 10px;border-radius:999px;background:#fff;border:1px solid #e5e7eb;color:#64748b;box-shadow:var(--shadow);font-size:12px;margin-top:8px}
</style>
</head>
<body>
<div class="wrap">
  <header>
    <div class="logo">AJ</div>
    <div>
      <h1>ESP Sensor Dashboard</h1>
      <div class="subtitle">ESP32 + DHT22 + DS18B20 + BH1750</div>
    </div>
  </header>

  <div class="grid">
    <section class="card">
      <div class="icon temp">T</div>
      <div class="label">Temperature (DHT)</div>
      <div class="value"><div class="num">%s</div><div class="unit">°C</div></div>
      <div class="chip">Real-time</div>
    </section>

    <section class="card">
      <div class="icon hum">H</div>
      <div class="label">Humidity</div>
      <div class="value"><div class="num">%s</div><div class="unit">%%</div></div>
      <div class="chip">Indoor</div>
    </section>

    <section class="card">
      <div class="icon ds">DS</div>
      <div class="label">Temperature (DS)</div>
      <div class="value"><div class="num">%s</div><div class="unit">°C</div></div>
      <div class="chip">DS18B20</div>
    </section>
  </div>

  <footer>Updated: %s</footer>
</div>
</body>
</html>
""" % (
        "-" if temp is None else temp,
        "-" if hum is None else hum,
        "-" if ds_temp is None else ds_temp,
        timestamp
    )

# ===== 6) WEB SERVER =====
def start_server():
    addr = socket.getaddrinfo("0.0.0.0", 80)[0][-1]
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen(2)
    print("Listening on", addr)

    while True:
        try:
            cl, remote = s.accept()
            # print("Client:", remote)
            req = cl.recv(1024)
            # ทำ endpoint ง่าย ๆ: /api/json สำหรับดึงค่าดิบ
            req_str = req.decode()
            if "GET /api/json" in req_str:
                t, h, td = read_sensors()
                body = '{"temp": %s, "hum": %s, "ds_temp": %s}' % (
                    "null" if t  is None else t,
                    "null" if h  is None else h,
                    "null" if td is None else td
                )
                cl.send("HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nCache-Control: no-store\r\n\r\n")
                cl.send(body)
                cl.close()
                # อัปเดต OLED ด้วย
                oled_show(t, h, td)
                continue

            # หน้า HTML
            t, h, td = read_sensors()
            html = pastel_html(t, h, td)
            cl.send("HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\nCache-Control: no-store\r\n\r\n")
            cl.sendall(html)
            cl.close()
            # อัปเดต OLED ด้วย
            oled_show(t, h, td)

        except Exception as e:
            try:
                cl.close()
            except:
                pass
            print("Socket error:", e)

# ===== 7) RUN =====
if __name__ == "__main__":
    wlan = wifi_connect()
    start_server()