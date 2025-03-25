from kafka import KafkaProducer
from faker import Faker
from json import dumps
from time import sleep, time
from random import uniform


# Set up Faker
fake = Faker()

# Kafka config
KAFKA_TOPIC = "fake-users"
KAFKA_BROKER = "kafka:9092"

# Set up Kafka producer
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER, value_serializer=lambda v: dumps(v).encode("utf-8")
)


def generate_fake_user():
    return {
        "id": fake.uuid4(),
        "name": fake.name(),
        "email": fake.email(),
        "address": fake.address(),
        "phone": fake.phone_number(),
        "dob": fake.date_of_birth(minimum_age=18, maximum_age=60).isoformat(),
        "created_at": fake.iso8601(),
    }

# Produce messages for a fixed amount of time
def produce_messages_upto(up_time: int = 60, delay: int = 1):
    print(
        f"Producing fake user messages to topic '{KAFKA_TOPIC}' for {up_time} seconds..."
    )
    start_time = time()
    try:
        while time() - start_time < up_time:
            user = generate_fake_user()
            producer.send(KAFKA_TOPIC, value=user)
            print(f"✅ Message sent - user name: {user['name']} & id: {user['id']}")
            sleep(round(uniform(0.5, delay), 1))  # Simulate processing time
    except KeyboardInterrupt:
        print("\nStopped producing.")
    finally:
        producer.flush()
        producer.close()
        print(f"Finished producing messages. Total time: {time() - start_time:.2f} seconds")

# Produce messages for a fixed number of times
def produce_messages(count=10, delay=1):
    print(f"Producing {count} fake user messages to topic '{KAFKA_TOPIC}'...")

    try:
        for _ in range(count):
            user = generate_fake_user()
            producer.send(KAFKA_TOPIC, value=user)
            print(f"✅ Message sent - user name: {user['name']} & id: {user['id']}")
            sleep(round(uniform(0.5, delay), 1))  # Simulate processing time
    except KeyboardInterrupt:
        print("\nStopped producing.")
    finally:
        producer.flush()
        producer.close()
        print("Finished producing messages.")


if __name__ == "__main__":
    # produce_messages(count=10, delay=4)  # You can change these 
    produce_messages_upto(10)  # You can change these
