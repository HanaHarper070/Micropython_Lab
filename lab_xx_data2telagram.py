import urequests

BOT_TOKEN = "7911554077:AAEano0zZ5zRHjzv1xl62eiM1WBN8Llqp9w"
CHAT_ID = "7480253626"

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

msg = ("🏡 In greenhouse 🪴")

send_telegram_message(msg)