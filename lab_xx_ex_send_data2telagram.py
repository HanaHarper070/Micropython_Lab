import urequests
import network
import gc

# ได้จากขั้นตอนที่ 1 และ 2
BOT_TOKEN = "8120042898:AAHFxt8mWmo8nT-1214rS-oEZsnxC6gK6Zk"
CHAT_ID = "7480253626"

# ฟังก์ชันการเชื่อมต่ออินเทอร์เน็ต
def wifi_connect():
    ssid = 'FM_IoT' 
    password = 'fm1234567890'
    station = network.WLAN(network.STA_IF)
    station.active(True)
    if not station.isconnected():
        station.connect(ssid, password)
        while not station.isconnected():
            pass
    print('WiFi connected:', station.ifconfig())

# ฟังก์ชันการส่งข้อมูลผ่าน HTTP requests
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = f"chat_id={CHAT_ID}&text={message}"
    try:
        response = urequests.post(url, data=payload.encode('utf-8'), headers=headers)
        print("Telegram response:", response.text)
        response.close()
        gc.collect()
    except Exception as e:
        print("Telegram error:", e)

wifi_connect() #การนำฟังก์ชันการเชื่อมต่ออินเทอร์เน็ตมาใช้

# ตัวอย่างข้อความจากเซนเซอร์
temperature = 30
humidity = 70
msg = f"สภาพอากาศวันนี้:\n\n🌡 Temperature: {temperature}°C\n\n💧 Humidity: {humidity}%"
send_telegram_message(msg) #การนำฟังก์ชันมาใช้ในการส่งข้อความขึ้น telegram