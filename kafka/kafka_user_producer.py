from kafka import KafkaProducer
from faker import Faker
from json import dumps
from time import sleep

fake = Faker()


# Kafka config
KAFKA_TOPIC = "fake-users"
KAFKA_BROKER = "kafka:9092"

# Set up Kafka producer
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: dumps(v).encode("utf-8")
)

def generate_fake_user():
    return {
        "id": fake.uuid4(),
        "name": fake.name(),
        "email": fake.email(),
        "address": fake.address(),
        "phone": fake.phone_number(),
        "dob": fake.date_of_birth(minimum_age=18, maximum_age=60).isoformat(),
        "created_at": fake.iso8601()
    }

def produce_messages(count=10, delay=1):
    print(f"Producing {count} fake user messages to topic '{KAFKA_TOPIC}'...")
    for _ in range(count):
        user = generate_fake_user()
        producer.send(KAFKA_TOPIC, value=user)
        print("Produced:", user)
        sleep(delay)

    producer.flush()
    print("Finished producing messages.")

if __name__ == "__main__":
    produce_messages(count=10, delay=2)  # You can change these values
