import random
from time import sleep

import pika
from actors import Actor
from utils.admin_payload import AdminPayload
from utils.examination_types import ExaminationStatus, ExaminationType
from utils.message_payload import MessagePayload
from utils.payload_types import parse_payload


class Technician(Actor):
    def __init__(self, examination_types: list[ExaminationType]) -> None:
        super().__init__()
        self.id = "technician_" + self.id
        self.examination_types = examination_types
        self.sending_channel.close()
        self.sending_connection.close()

    def run(self) -> None:
        try:
            self._listen_for_results()
        except Exception:
            return

    def _initialize_queues(self) -> None:
        self.id = "technician_" + self.id
        self.queue = self.id + "_queue"
        self.listening_channel.queue_declare(queue=self.queue, exclusive=True)
        self.listening_channel.queue_bind(
            exchange="admin_announcement_exchange",
            queue=self.queue,
        )

    def _listen_for_results(self) -> None:
        def callback(ch, method, props, body):
            payload = parse_payload(props.type, body.decode())

            payload.status = ExaminationStatus.DONE
            payload.source = self.id

            # Handling examination
            sleep(random.randint(2, 6))

            ch.basic_publish(
                exchange="",
                routing_key=props.reply_to,
                properties=pika.BasicProperties(
                    correlation_id=props.correlation_id,
                    type="message",
                ),
                body=payload.to_json(),
            )

            ch.basic_publish(
                exchange="admin_exchange",
                routing_key="",
                properties=pika.BasicProperties(
                    correlation_id=props.correlation_id,
                    type="message",
                ),
                body=payload.to_json(),
            )

            ch.basic_ack(delivery_tag=method.delivery_tag)

        def admin_callback(ch, method, props, body):
            payload = parse_payload(props.type, body.decode())
            payload.print_colored()
            ch.basic_ack(delivery_tag=method.delivery_tag)

        self.listening_channel.basic_qos(prefetch_count=1)
        for exam_type in self.examination_types:
            self.listening_channel.basic_consume(
                queue=f"{exam_type}_queue", on_message_callback=callback, auto_ack=False
            )
        self.listening_channel.basic_consume(
            queue=self.queue, on_message_callback=admin_callback, auto_ack=False
        )

        try:
            self.listening_channel.start_consuming()
        except Exception as e:
            return
        except KeyboardInterrupt as e:
            return
