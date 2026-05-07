from twilio.rest import Client
import os

ACCOUNT_SID = os.getenv("ACCOUNT_SID") or "your_sid"
AUTH_TOKEN = os.getenv("AUTH_TOKEN") or "your_token"

TWILIO_NUMBER = "+18259069663"   # ✅ FIXED
YOUR_NUMBER = "+916360237740"

client = Client(ACCOUNT_SID, AUTH_TOKEN)

sms_count = 0
MAX_SMS = 5

def send_notification(message):
    global sms_count

    try:
        print("📤 Attempting SMS:", message)

        if not any(keyword in message.lower() for keyword in ["low sales", "anomaly"]):
            print("ℹ️ Skipping non-critical alert")
            return

        if sms_count >= MAX_SMS:
            print("⚠️ SMS limit reached")
            return

        msg = client.messages.create(
            body=message,
            from_=TWILIO_NUMBER,
            to=YOUR_NUMBER
        )

        sms_count += 1
        print(f"📩 SMS sent ({sms_count}/{MAX_SMS}) → {msg.sid}")

    except Exception as e:
        print("❌ SMS failed:", str(e))