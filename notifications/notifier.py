from twilio.rest import Client
import os

ACCOUNT_SID = os.getenv("ACCOUNT_SID")
AUTH_TOKEN = os.getenv("AUTH_TOKEN")
TWILIO_NUMBER = "(825) 906-9663"
YOUR_NUMBER = "+916360237740"

client = Client(ACCOUNT_SID, AUTH_TOKEN)

sms_count = 0
MAX_SMS = 5

def send_notification(message):
    global sms_count

    try:
        # ✅ Case-insensitive check
        if "low sales" not in message.lower():
            print("ℹ️ Skipping non-critical alert")
            return

        # ✅ Limit control
        if sms_count >= MAX_SMS:
            print("⚠️ SMS limit reached for this run")
            return

        # ✅ Send SMS
        msg = client.messages.create(
            body=message,
            from_=TWILIO_NUMBER,
            to=YOUR_NUMBER
        )

        sms_count += 1
        print(f"📩 SMS sent ({sms_count}/{MAX_SMS}) → {msg.sid}")

    except Exception as e:
        print("❌ SMS failed:", str(e))