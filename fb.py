import os
import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

COMPANY_NAME = "GM & Sons Solutions"

# Meta WhatsApp API Credentials (aap inhein environment variables mein bhi daal sakte hain)
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN", "YAHAN_APNA_ACCESS_TOKEN_DALNA")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID", "YAHAN_PHONE_NUMBER_ID_DALNA")
VERIFY_TOKEN = "gmsons_verify_token_123"

SERVICES_MENU = (
    "👋 Assalam-o-Alaikum! Welcome to *GM & Sons Solutions*.\n"
    "We provide professional digital services and automation solutions. Here is"
    " our service menu & pricing:\n\n"
    "1️⃣ *Automated WhatsApp Ordering & Support Bot*\n"
    "   - Direct WhatsApp message automation, welcome greetings, and"
    " interactive menus.\n"
    "   - 💰 Charges: PKR 15,000 (One-time setup)\n\n"
    "2️⃣ *School Management System & Software*\n"
    "   - Student performance tracking, attendance progress visualizations,"
    " and fee payment workflows.\n"
    "   - 💰 Charges: PKR 35,000 (Complete package)\n\n"
    "3️⃣ *Customized Game with Your Child (Interactive Family Game)*\n"
    "   - Personalized interactive mini-games featuring your child's name"
    " and custom fun elements.\n"
    "   - 💰 Charges: PKR 8,000 per game\n\n"
    "4️⃣ *Digital Services & Tech Consultation*\n"
    "   - Custom software solutions, web setups, and technical support.\n"
    "   - 💰 Charges: PKR 5,000 / consultation or project basis\n\n"
    "Reply with the service number (1-4) or your specific requirement, and"
    " our team will get back to you!"
)


@app.route("/", methods=["GET"])
def home():
  return f"{COMPANY_NAME} WhatsApp Bot Server is live and running successfully!"


@app.route("/webhook", methods=["GET"])
def verify_whatsapp_webhook():
  mode = request.args.get("hub.mode")
  token = request.args.get("hub.verify_token")
  challenge = request.args.get("hub.challenge")

  if mode and token:
    if mode == "subscribe" and token == VERIFY_TOKEN:
      return challenge, 200
    else:
      return "Verification token is invalid", 403
  return "Webhook endpoint is active", 200


@app.route("/webhook", methods=["POST"])
def handle_whatsapp_messages():
  incoming_data = request.json
  print("Incoming WhatsApp Data:", incoming_data)

  try:
    entries = incoming_data.get("entry", [])
    for entry in entries:
      changes = entry.get("changes", [])
      for change in changes:
        value = change.get("value", {})
        messages = value.get("messages", [])
        if messages:
          sender_number = messages[0].get("from")

          # Meta WhatsApp Cloud API URL to send message back
          url = f"https://graph.facebook.com/v17.0/{PHONE_NUMBER_ID}/messages"
          headers = {
              "Authorization": f"Bearer {WHATSAPP_TOKEN}",
              "Content-Type": "application/json",
          }
          payload = {
              "messaging_product": "whatsapp",
              "to": sender_number,
              "type": "text",
              "text": {"body": SERVICES_MENU},
          }

          response = requests.post(url, json=payload, headers=headers)
          print("WhatsApp Send Response:", response.json())

    return jsonify({"status": "success"}), 200

  except Exception as e:
    print("Error handling message:", e)
    return jsonify({"status": "error", "error_message": str(e)}), 400


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
