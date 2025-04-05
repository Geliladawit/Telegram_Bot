from flask import Flask, request
import logging
import requests
import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")  

logging.basicConfig(level=logging.INFO)

if BOT_TOKEN and WEBHOOK_URL:
    response = requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook",
        data={"url": WEBHOOK_URL}
    )
    logging.info("Webhook set: %s", response.json())
else:
    logging.warning("BOT_TOKEN or WEBHOOK_URL not set!")

app = Flask(__name__)
TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

@app.route('/', methods=['GET'])
def home():
    return "Webhook server running!"

@app.route('/webhook', methods=['POST'])
def telegram_webhook():
    data = request.get_json()
    logging.info("Received update: %s", data)

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")
        reply_text = f"You said: {text}"

        # Respond back to Telegram
        requests.post(f"{TELEGRAM_API_URL}/sendMessage", json={
            "chat_id": chat_id,
            "text": reply_text
        })

    return 'OK', 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
