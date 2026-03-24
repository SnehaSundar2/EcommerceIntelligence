from kafka import KafkaConsumer
from notifications.notifier import send_notification

consumer = KafkaConsumer(
    'trending',
    'low_sales',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    group_id='ecommerce-group',
    value_deserializer=lambda x: x.decode('utf-8')
)

print("🚀 Listening for Kafka events...")

for message in consumer:
    msg = message.value
    print(f"Received → {msg}")

    send_notification(msg)   # Email / SMS / WhatsApp