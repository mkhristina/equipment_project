
import json
import os

import pika


RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "guest")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD", "guest")

QUEUE_NAME = "maintenance_requests"


def send_maintenance_event(event_data: dict):
    """
    Отправляет событие о новой заявке в RabbitMQ.
    """

    credentials = pika.PlainCredentials(
        username=RABBITMQ_USER,
        password=RABBITMQ_PASSWORD
    )

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=RABBITMQ_HOST,
            credentials=credentials
        )
    )

    try:
        channel = connection.channel()

        channel.queue_declare(
            queue=QUEUE_NAME,
            durable=True
        )

        message = json.dumps(
            event_data,
            ensure_ascii=False
        )

        channel.basic_publish(
            exchange="",
            routing_key=QUEUE_NAME,
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=2
            )
        )

        print("Событие отправлено в RabbitMQ:", message)

    finally:
        connection.close()
