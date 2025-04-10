from json import loads
from kafka import KafkaConsumer
from kafka.consumer.fetcher import ConsumerRecord
from random import uniform
from time import sleep
from typing import Callable


# Kafka config
KAFKA_TOPIC = "fake-users"
KAFKA_BROKER = "kafka:29092"
GROUP_ID = "user-consumer-group"


# Set up Kafka consumer
def get_kafka_consumer():
    # Value deserializer function
    fn_value_deserializer: Callable[[bytes], dict[str, str]] = lambda v: loads(
        v.decode("utf-8")
    )

    return KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BROKER,
        auto_offset_reset="earliest",
        group_id=GROUP_ID,
        enable_auto_commit=False,
        value_deserializer=fn_value_deserializer,
        consumer_timeout_ms=25_000,  # wait for messages for 25 seconds
        session_timeout_ms=30_000,  # rejoin group if session times out
        heartbeat_interval_ms=10_000,  # send heartbeat every 10 seconds
    )


consumer = get_kafka_consumer()  # Set up Kafka consumer


def consume_messages(delay=1):
    print(f"Started consuming messages from topic '{KAFKA_TOPIC}'...")

    try:
        for message in consumer:
            message: ConsumerRecord
            user = message.value
            print(f"📩 Received message - user name: {user['name']} & id: {user['id']}")
            consumer.commit()  # Commit the message to the Kafka broker
            sleep(round(uniform(1, delay), 1))  # Simulate processing time
    except KeyboardInterrupt:
        print("\nStopped consuming.")
    finally:
        consumer.close()
        print("Finished consuming messages.")

    return "Consumed messages."


if __name__ == "__main__":
    consume_messages(delay=4)  # You can change these values
