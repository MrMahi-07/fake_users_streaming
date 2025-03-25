from json import loads
from kafka import KafkaConsumer
from kafka.consumer.fetcher import ConsumerRecord
from random import uniform
from time import sleep
from typing import Callable


# Kafka config
KAFKA_TOPIC = "fake-users"
KAFKA_BROKER = "kafka:9092"
GROUP_ID = "user-consumer-group"

fn_value_deserializer: Callable[[bytes], dict[str, str]] = lambda v: loads(
    v.decode("utf-8")
)

# Set up Kafka consumer
consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=KAFKA_BROKER,
    auto_offset_reset="earliest",
    group_id=GROUP_ID,
    enable_auto_commit=True,
    value_deserializer=fn_value_deserializer,
    consumer_timeout_ms=10_000,  # Stop after 10 seconds of inactivity
)
consumer.subscribe([KAFKA_TOPIC])


def consume_messages(delay=1):
    print(f"Started consuming messages from topic '{KAFKA_TOPIC}'...")

    try:
        for message in consumer:
            message: ConsumerRecord
            user = message.value
            print(f"📩 Received message - user name: {user['name']} & id: {user['id']}")
            sleep(round(uniform(1, delay), 1))  # Simulate processing time
    except KeyboardInterrupt:
        print("\nStopped consuming.")
    finally:
        consumer.close()
        print("Finished consuming messages.")


if __name__ == "__main__":
    consume_messages(delay=4)  # You can change these values
