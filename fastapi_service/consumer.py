
import json
import os

import pika


RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "guest")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD", "guest")

QUEUE_NAME = "maintenance_requests"


def callback(ch, method, properties, body):
    """
    Обрабатывает полученное сообщение из RabbitMQ.
    """

    event_data = json.loads(body.decode("utf-8"))

    print("\nПолучено новое событие:")
    print(json.dumps(
        event_data,
        ensure_ascii=False,
        indent=4
    ))

    ch.basic_ack(
        delivery_tag=method.delivery_tag
    )


def main():
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

    channel = connection.channel()

    channel.queue_declare(
        queue=QUEUE_NAME,
        durable=True
    )

    channel.basic_qos(prefetch_count=1)

    channel.basic_consume(
        queue=QUEUE_NAME,
        on_message_callback=callback
    )

    print("Consumer запущен. Ожидание сообщений...")

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("\nConsumer остановлен.")
        channel.stop_consuming()
    finally:
        connection.close()


if __name__ == "__main__":
    main()
