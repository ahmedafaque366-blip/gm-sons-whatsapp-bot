from flask import Flask, request, jsonify

app = Flask(__name__)

# GM & Sons Solutions - Business Details & Services Menu with Dummy Charges
COMPANY_NAME = "GM & Sons Solutions"

SERVICES_MENU = (
    "👋 Assalam-o-Alaikum! Welcome to *GM & Sons Solutions*.\n"
    "We provide professional digital services and automation solutions. Here is our service menu & pricing:\n\n"
    "1️⃣ *Automated WhatsApp Ordering & Support Bot*\n"
    "   - Direct WhatsApp message automation, welcome greetings, and interactive menus.\n"
    "   - 💰 Charges: PKR 15,000 (One-time setup)\n\n"
    "2️⃣ *School Management System & Software*\n"
    "   - Student performance tracking, attendance progress visualizations, and fee payment workflows.\n"
    "   - 💰 Charges: PKR 35,000 (Complete package)\n\n"
    "3️⃣ *Customized Game with Your Child (Interactive Family Game)*\n"
    "   - Personalized interactive mini-games featuring your child's name and custom fun elements.\n"
    "   - 💰 Charges: PKR 8,000 per game\n\n"
    "4️⃣ *Digital Services & Tech Consultation*\n"
    "   - Custom software solutions, web setups, and technical support.\n"
    "   - 💰 Charges: PKR 5,000 / consultation or project basis\n\n"
    "Reply with the service number (1-4) or your specific requirement, and our team will get back to you!"
)

@app.route("/", methods=["GET"])
def home():
    return f"{COMPANY_NAME} WhatsApp Bot Server is live and running successfully!"

# Meta Webhook Verification (WhatsApp API ke liye)
@app.route("/webhook", methods=["GET"])
def verify_whatsapp_webhook():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    
    # Aapka custom verify token
    if mode and token:
        if mode == "subscribe" and token == "gmsons_verify_token_123":
            return challenge, 200
        else:
            return "Verification token is invalid", 403
    return "Webhook endpoint is active", 200

# Incoming WhatsApp Messages ko handle karne ke liye POST webhook
@app.route("/webhook", methods=["POST"])
def handle_whatsapp_messages():
    incoming_data = request.json
    print("Incoming WhatsApp Data:", incoming_data)
    
    try:
        # Yahan par user ka incoming message parse hota hai. 
        # Jab koi client message karega, toh yeh code menu aur charges wapas bhejega.
        
        response_payload = {
            "messaging_product": "whatsapp",
            "status": "success",
            "bot_response": SERVICES_MENU
        }
        return jsonify(response_payload), 200

    except Exception as e:
        print("Error handling message:", e)
        return jsonify({"status": "error", "error_message": str(e)}), 400

if __name__ == "__main__":
    app.run(port=5000, debug=True)