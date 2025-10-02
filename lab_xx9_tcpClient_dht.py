# tcpClient_dht.py
import network, socket, time, ujson
from machine import Pin
import dht

SSID = "FM_IoT"
PASSWORD = "fm1234567890"

HOST = "192.168.188.100"  
PORT = 10000

PIN_DHT = 14            

WIFI_WAIT_SEC = 20      
RECV_TIMEOUT = 3       
SEND_PERIOD = 2         

sensor = dht.DHT22(Pin(PIN_DHT))

def connect_wifi(ssid, passwd, wait_s=WIFI_WAIT_SEC):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connecting WiFi...")
        wlan.connect(ssid, passwd)
        t0 = time.ticks_ms()
        while not wlan.isconnected():
            if time.ticks_diff(time.ticks_ms(), t0) > wait_s * 1000:
                raise OSError("WiFi connect timeout")
            time.sleep(1)
    print("WiFi connected:", wlan.ifconfig())
    return wlan

def connect_server(host, port):
    s = socket.socket()
    try:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    except:
        pass
    s.settimeout(RECV_TIMEOUT)  
    print("Connecting TCP...", host, port)
    s.connect((host, port))
    print("TCP connected")
    return s

def safe_recv_json(sock):
    """พยายาม recv; ถ้าไม่มีข้อมูลในเวลาที่กำหนดจะคืน None"""
    try:
        data = sock.recv(1024)
        if not data:
            return None
        try:
            text = data.decode("utf-8")
        except:
            text = str(data)
        return ujson.loads(text)
    except (OSError, ValueError):
        # timeout / parse error / no data
        return None

def main():
    wlan = None
    sock = None
    while True:
        try:
            # 1) Wi-Fi
            if (wlan is None) or (not wlan.isconnected()):
                wlan = connect_wifi(SSID, PASSWORD)

            # 2) TCP
            if sock is None:
                sock = connect_server(HOST, PORT)

            # 3) อ่านเซนเซอร์
            sensor.measure()
            temp = sensor.temperature()
            humi = sensor.humidity()
            temp = round(temp, 2)
            humi = round(humi, 2)
            meas = [temp, humi]
            payload = ujson.dumps(meas)  + "\n"# → str
            #payload = ujson.dumps([temp, humi]) + "\n"
            
            # 4) ส่ง
            # แปลงเป็น bytes; ต่อท้าย newline ก็ได้ถ้า server ใช้แบบบรรทัด
            sock.send(payload.encode("utf-8"))
            # sock.send((payload + "\n").encode())  # <— ถ้า server อ่านทีละบรรทัด
            print("sent:", payload)

            # 5) (ทางเลือก) รับคำตอบจาก server ถ้ามี
            reply = safe_recv_json(sock)
            if reply is not None:
                try:
                    print("echo temp: %.1f" % float(reply[0]))
                    print("echo humi: %.1f" % float(reply[1]))
                except Exception:
                    print("reply:", reply)
            time.sleep(SEND_PERIOD)

        except OSError as e:
            print("OSError:", e)
            try:
                if sock:
                    sock.close()
            except:
                pass
            sock = None
            time.sleep(2)
        except Exception as e:
            print("Error:", repr(e))
            try:
                if sock:
                    sock.close()
            except:
                pass
            sock = None
            time.sleep(2)

if __name__ == "__main__":
    main()