from kafka import KafkaProducer
import time

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: v.encode('utf-8')
)

def send_event(topic, message):
    print(f"Sending → {message}")   # 👈 show in terminal
    producer.send(topic, message)
    producer.flush()

    time.sleep(2)   # ⏳ simulate real-time delay