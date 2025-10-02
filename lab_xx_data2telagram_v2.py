import network
from time import sleep
from telegram_bot import TelegramBot # Import the new class

# --- Wi-Fi Connection (Required) ---
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

# --- Credentials ---
BOT_TOKEN = "8127425365:AAFdBxngLFmMr83jAoikGJlP2pisTJEdkKo"
CHAT_ID = "7480253626"

# --- Main Program ---
wifi_connect()

# Create an instance of your bot
bot = TelegramBot(BOT_TOKEN, CHAT_ID)

# Send a simple message
print("\n--- Sending a test message ---")

temperature = 30
humidity = 70
light = 500
soilmc = 40

msg = (
    "🏡 สภาพอากาศวันนี้ 🪴:\n\n"
    f"🌡 Temp: {temperature}°C\n\n"
    f"💧Humidity: {humidity}%\n\n"
    f"☀ Light: {light} lux\n\n"
    f"🌱 Soil Moisture: {soilmc}%"
)


bot.send_message(msg)