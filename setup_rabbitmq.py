import pika

from utils.examination_types import ExaminationType


def setup_rabbitmq():
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()

    channel.exchange_declare(exchange="exam_exchange", exchange_type="direct")

    channel.exchange_declare(exchange="admin_exchange", exchange_type="fanout")

    channel.exchange_declare(
        exchange="admin_announcement_exchange", exchange_type="fanout"
    )

    for exam_type in ExaminationType:
        channel.queue_declare(queue=exam_type.to_queue_name())
        channel.queue_bind(
            exchange="exam_exchange",
            queue=exam_type.to_queue_name(),
            routing_key=exam_type,
        )

    channel.queue_declare(queue="admin_queue")
    channel.queue_bind(exchange="admin_exchange", queue="admin_queue")

    connection.close()


if __name__ == "__main__":
    setup_rabbitmq()
