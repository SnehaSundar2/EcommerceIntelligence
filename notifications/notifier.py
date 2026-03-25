from twilio.rest import Client
import os

# 🔑 Replace with your credentials
ACCOUNT_SID = os.getenv("ACCOUNT_SID")
AUTH_TOKEN = os.getenv("AUTH_TOKEN")
TWILIO_NUMBER = "(825) 906-9663"   # Twilio number
YOUR_NUMBER = "+916360237740"   # Your phone

client = Client(ACCOUNT_SID, AUTH_TOKEN)

# 🔢 Limit SMS count per run
sms_count = 0
MAX_SMS = 5   # change if needed

def send_notification(message):
    global sms_count

    try:
        # 🚨 Send ONLY critical alerts (low sales)
        if "Low sales" not in message:
            print("ℹ️ Skipping non-critical alert")
            return

        # 🚫 Prevent exceeding limit
        if sms_count >= MAX_SMS:
            print("⚠️ SMS limit reached for this run")
            return

        # 📩 Send SMS
        msg = client.messages.create(
            body=message,
            from_=TWILIO_NUMBER,
            to=YOUR_NUMBER
        )

        sms_count += 1
        print(f"📩 SMS sent ({sms_count}/{MAX_SMS}) → {msg.sid}")

    except Exception as e:
        print("❌ SMS failed:", e)