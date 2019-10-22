
from kafka import KafkaProducer
import os

value_bytes = bytes('this is a kafka test', encoding='utf-8')
KAFKA_PRODUCER = KafkaProducer(bootstrap_servers=['192.168.1.66:9092,192.168.1.67:9092'], api_version=(0, 10))
print(KAFKA_PRODUCER)
KAFKA_PRODUCER.send(os.environ['KF_TOPIC'], value_bytes)
print("message sent")