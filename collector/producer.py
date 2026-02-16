import json
import time
import requests
from kafka import KafkaProducer

KAFKA_BOOTSTRAP = "kafka:9092"
TOPIC = "api-events"

producer = None
while producer is None:
    try:
        producer = KafkaProducer(
            bootstrap_servers=KAFKA_BOOTSTRAP,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            api_version_auto_timeout_ms=10000,
            request_timeout_ms=10000,
        )
        print("✅ Connecté à Kafka")
    except Exception as e:
        print("⏳ Kafka pas prêt, nouvelle tentative dans 5s...", e)
        time.sleep(5)


API_URL = "https://api.open-meteo.com/v1/forecast?latitude=48.85&longitude=2.35&current_weather=true"

while True:
    try:
        response = requests.get(API_URL)
        data = response.json()

        event = {
            "city": "Paris",
            "temp": data["current_weather"]["temperature"],
            "description": "live_weather",
            "timestamp": data["current_weather"]["time"],
            "source": "open-meteo"
        }

        producer.send(TOPIC, event)
        print("Sent:", event)

        time.sleep(10)

    except Exception as e:
        print("Error:", e)
        time.sleep(5)
