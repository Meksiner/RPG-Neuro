from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from kafka import KafkaProducer, KafkaConsumer
import uuid
import os

# Config API
app = Flask(__name__)
socketio = SocketIO(app)
# Config model
BOOTSTRAP_SERVERS = os.environ.get("KAFKA_BROKER_URL")  # e.g., 'kafka:9092'
TOPIC_NAME = os.environ.get("TRANSACTIONS_TOPIC")
MODEL_TOPIC = os.environ.get("MODEL_TOPIC")

# Local config :
# BOOTSTRAP_SERVERS = "localhost:9092"
# TOPIC_NAME = "test"
# MODEL_TOPIC = "model"


@app.route("/")
def home():
    return render_template("index.html")


""" Kafka endpoints """


@socketio.on("connect", namespace="/kafka")
def test_connect():
    print('Connected via Websocket')


def kafkaconsumer():
    consumer = KafkaConsumer(
        TOPIC_NAME,
        bootstrap_servers=BOOTSTRAP_SERVERS,
        auto_offset_reset="latest",
        enable_auto_commit=True,
        group_id='my-group'  # specify a group id to enable consumer group behavior
    )

    # Poll for new messages (blocking)
    for message in consumer:
        msg = message.value.decode("utf-8")
        response = chatbot(msg)
        print(response)
        emit("kafkaconsumer", response)
        # Assuming you want to process only the latest message, break after one
        break

    consumer.close()


@socketio.on("kafkaproducer", namespace="/kafka")
def kafkaproducer(message):
    producer = KafkaProducer(bootstrap_servers=BOOTSTRAP_SERVERS)
    producer.send(
        TOPIC_NAME,
        value=bytes(str(message), encoding="utf-8"),
        key=bytes(str(uuid.uuid4()), encoding="utf-8"),
    )
    producer.close()
    kafkaconsumer()


if __name__ == "__main__":
    from kafka_model import chatbot
    socketio.run(app, host="0.0.0.0", port=80, allow_unsafe_werkzeug=True)
