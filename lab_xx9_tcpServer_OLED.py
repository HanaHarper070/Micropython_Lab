tcpServer_OLED.py
# tcpServer_OLED_fixed.py  (MicroPython / ESP32-C3 mini)
import network, socket, time, ujson, gc
from machine import Pin, SoftI2C
import ssd1306

SSID = "FM_IoT"
PASSWORD = "fm1234567890"
PORT = 10000

# I2C สำหรับจอ OLED (ปรับตามบอร์ดของคุณได้)
i2c = SoftI2C(scl=Pin(9), sda=Pin(10), freq=400000)  # ESP32-C3 mini (ตัวอย่าง)
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

def wifi_connect(ssid, passwd, timeout=20):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connecting WiFi...")
        wlan.connect(ssid, passwd)
        t0 = time.ticks_ms()
        while not wlan.isconnected():
            if time.ticks_diff(time.ticks_ms(), t0) > timeout * 1000:
                raise OSError("WiFi connect timeout")
            time.sleep(1)
    print("WiFi connected:", wlan.ifconfig())
    return wlan

def draw_waiting(ip):
    oled.fill(0)
    oled.text("Server Ready", 10, 5)
    oled.text(ip, 2, 20)
    oled.text("Waiting for", 10, 36)
    oled.text("connections...", 2, 48)
    oled.show()

def draw_values(temperature, humidity):
    oled.fill(0)
    oled.text("Weather Farm 01", 2, 5)
    try:
        oled.text("Temp: %.1f C" % float(temperature), 2, 24)
    except:
        oled.text("Temp: -", 2, 24)
    try:
        oled.text("Humi: %.1f %%" % float(humidity), 2, 40)
    except:
        oled.text("Humi: -", 2, 40)
    oled.show()

def serve():
    wlan = wifi_connect(SSID, PASSWORD)
    ip_address = wlan.ifconfig()[0]
    print("Server IP address:", ip_address)
    draw_waiting(ip_address)

    srv = socket.socket()
    try:
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    except:
        pass
    srv.bind((ip_address, PORT))
    srv.listen(1)
    print("TCP server listening on", ip_address, PORT)

    while True:
        print("Accepting connections...")
        conn, addr = srv.accept()
        print(addr, "connected")
        try:
            conn.settimeout(5)  # กัน recv ค้าง
            buf = b""           # buffer สำหรับสะสมข้อมูล

            while True:
                try:
                    data = conn.recv(1024)
                    if not data:
                        print("Client closed")
                        break
                    buf += data

                    # 1) กรณีใช้ newline-delimited JSON: อ่านทีละบรรทัด
                    while b"\n" in buf:
                        line, buf = buf.split(b"\n", 1)
                        if not line:
                            continue
                        try:
                            obj = ujson.loads(line.decode())
                            temperature, humidity = obj[0], obj[1]
                            print("Received (line):", temperature, humidity)
                            draw_values(temperature, humidity)
                            # echo back (ตามโปรโตคอลเดิม)
                            conn.send((ujson.dumps([temperature, humidity]) + "\n").encode())
                        except Exception as e:
                            print("JSON line parse error:", e)

                    # 2) กรณีไม่มี newline: ลอง parse ทั้ง buffer แบบ best-effort
                    if buf and b"\n" not in buf:
                        try:
                            obj = ujson.loads(buf.decode())
                            buf = b""  # consume ทั้งหมด
                            temperature, humidity = obj[0], obj[1]
                            print("Received (raw):", temperature, humidity)
                            draw_values(temperature, humidity)
                            conn.send((ujson.dumps([temperature, humidity]) + "\n").encode())
                        except Exception:
                            # ยัง parse ไม่ได้ อาจยังมาไม่ครบ → รอ recv รอบถัดไป
                            pass

                except OSError as e:
                    # timeout/ข้อผิดพลาด socket เล็กน้อย → เว้นแล้ววนรอ
                    # print("Socket OSError:", e)
                    pass
                gc.collect()

        finally:
            try:
                conn.close()
            except:
                pass
            draw_waiting(ip_address)

# Run server
serve()