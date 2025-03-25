from kafka import KafkaConsumer
from json import loads
from typing import Callable
from kafka.consumer.fetcher import ConsumerRecord

# Kafka config
KAFKA_TOPIC = "fake-users"
KAFKA_BROKER = "localhost:9092"
GROUP_ID = "user-consumer-group"

fn_value_deserializer: Callable[[bytes], dict[str,str]] = lambda v: loads(v.decode("utf-8"))

# Set up Kafka consumer
consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=KAFKA_BROKER,
    auto_offset_reset='earliest',  # Start from beginning if no offset
    group_id=GROUP_ID,
    enable_auto_commit=True,
    value_deserializer= fn_value_deserializer
)

print(f"Started consuming messages from topic '{KAFKA_TOPIC}'...")

try:
    for message in consumer:         
        user = message.value
        print("Consumed:", consumer)
except KeyboardInterrupt:
    print("\nStopped consuming.")

