from kafka import KafkaConsumer
from notifications.notifier import send_notification
import time

# ✅ Prevent startup race condition (Kafka not ready)
time.sleep(5)

consumer = KafkaConsumer(
    'trending',
    'low_sales',
    'anomaly',
    'recommendation',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    group_id='ecommerce-group',
    enable_auto_commit=True,
    value_deserializer=lambda x: x.decode('utf-8')
)

print("🚀 Listening for Kafka events...")

# ✅ Track sent alerts to avoid duplicates
sent_cache = set()

try:
    for message in consumer:
        msg = message.value
        topic = message.topic

        print(f"📥 Topic: {topic} | Message: {msg}")

        # =========================
        # 🧠 SMART FILTERING LOGIC
        # =========================

        # Avoid duplicate alerts
        if msg in sent_cache:
            print("⚠️ Duplicate skipped")
            continue

        # Limit cache size
        if len(sent_cache) > 100:
            sent_cache.clear()

        # =========================
        # 🎯 PRIORITY HANDLING
        # =========================

        if topic == "anomaly":
            print("🚨 HIGH PRIORITY ALERT")
            send_notification(f"🚨 ANOMALY DETECTED:\n{msg}")

        elif topic == "low_sales":
            print("⚠️ MEDIUM PRIORITY ALERT")
            send_notification(f"⚠️ LOW SALES ALERT:\n{msg}")

        elif topic == "recommendation":
            print("💡 Recommendation received (no SMS)")
            # Optional: store or log only
            # send_notification(msg)  # Uncomment if needed

        elif topic == "trending":
            print("📈 Trending update (no alert)")
            # No SMS to avoid spam

        # Save message in cache
        sent_cache.add(msg)

except KeyboardInterrupt:
    print("🛑 Consumer stopped manually")

except Exception as e:
    print("❌ Error in consumer:", str(e))

finally:
    consumer.close()
    print("🔌 Kafka consumer closed")