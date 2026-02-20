import json
import time
import requests
from kafka import KafkaProducer

KAFKA_BOOTSTRAP = "kafka:9092"
TOPIC = "api-events"

CITIES = [
    {"city": "Paris", "lat": 48.85, "lon": 2.35},
    {"city": "Lyon",  "lat": 45.76, "lon": 4.84},
]

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

def fetch_city_weather(city, lat, lon):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    data = r.json()
    cw = data["current_weather"]
    return {
        "city": city,
        "temp": cw["temperature"],
        "description": "live_weather",
        "timestamp": cw["time"],
        "source": "open-meteo",
    }

while True:
    try:
        for c in CITIES:
            event = fetch_city_weather(c["city"], c["lat"], c["lon"])
            producer.send(TOPIC, event)
            print("Sent:", event)

        producer.flush()
        time.sleep(10)

    except Exception as e:
        print("Error:", e)
        time.sleep(5)