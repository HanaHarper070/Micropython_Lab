import urequests
import network
import gc

BOT_TOKEN = "8127425365:AAFdBxngLFmMr83jAoikGJlP2pisTJEdkKo"
CHAT_ID = "7480253626"

def wifi_connect():
    ssid = 'Hana_Harpel22.4G'
    password = 'hanaharper2513'
    station = network.WLAN(network.STA_IF)
    station.active(True)
    if not station.isconnected():
        print('Connecting to WiFi...')
        station.connect(ssid, password)
        while not station.isconnected():
            pass
    print('WiFi connected:', station.ifconfig())

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

wifi_connect()

temperature = 30
humidity = 70
light = 500
soilmc = 40

msg = (
    "🏡 In greenhouse 🪴:\n\n"
    f"🌡 Temp: {temperature}°C\n\n"
    f"💧Humidity: {humidity}%\n\n"
    f"☀ Light: {light} lux\n\n"
    f"🌱 Soil Moisture: {soilmc}%"
)

send_telegram_message(msg)