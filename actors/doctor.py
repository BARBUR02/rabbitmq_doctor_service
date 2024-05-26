import threading
import uuid

import pika

from actors import Actor
from utils.examination_types import ExaminationType
from utils.message_payload import MessagePayload
from utils.payload_types import parse_payload


class Doctor(Actor):
    def __init__(self) -> None:
        self.callback_queue = None
        self.admin_queue = None
        super().__init__()
        self.id = "doctor_" + self.id
        self.correlation_ids: set[str] = set()

    def run(self) -> None:
        result_thread = threading.Thread(target=self._listen_for_results)
        result_thread.start()

        self._run_orders()

        try:
            self.listening_channel.stop_consuming()
        except Exception:
            pass

        result_thread.join()
        self._destruct()

    def _initialize_queues(self) -> None:
        response = self.listening_channel.queue_declare(
            queue=f"{self.id}_queue", exclusive=True
        )
        self.callback_queue = response.method.queue

        self.admin_queue = self.id + "admin_queue"
        self.listening_channel.queue_declare(queue=self.admin_queue, exclusive=True)
        self.listening_channel.queue_bind(
            exchange="admin_announcement_exchange",
            queue=self.admin_queue,
        )

    def _listen_for_results(self) -> None:
        def callback(ch, method, props, body):
            if props.correlation_id not in self.correlation_ids:
                print(f"Got unexpected correlation_id {props.correlation_id}")
            else:
                self.correlation_ids.remove(props.correlation_id)
                payload = parse_payload(props.type, body.decode())
                payload.print_colored()
                print()
                ch.basic_ack(delivery_tag=method.delivery_tag)

        def admin_callback(ch, method, props, body):
            payload = parse_payload(props.type, body.decode())
            payload.print_colored()
            print()
            ch.basic_ack(delivery_tag=method.delivery_tag)

        self.listening_channel.basic_consume(
            queue=self.callback_queue, on_message_callback=callback, auto_ack=False
        )
        self.listening_channel.basic_consume(
            queue=self.admin_queue, on_message_callback=admin_callback, auto_ack=False
        )

        try:
            self.listening_channel.start_consuming()
        except Exception:
            return

    def _run_orders(self) -> None:
        while True:
            try:
                raw_input = input()
                if not raw_input:
                    continue
                if raw_input == "examinations":
                    print(f"Awaiting:\n\t {' '.join(self.correlation_ids)} ")
                elif message := MessagePayload.parse_messages_payload(
                    self.id, raw_input
                ):
                    self._send_message(message)
                else:
                    print(
                        f"Incorrect examination type, or not patient name provided choose one from {' '.join([exam_type for exam_type in ExaminationType])}"
                    )

            except KeyboardInterrupt:
                break

    def _send_message(self, message: MessagePayload) -> None:
        correlation_id = str(uuid.uuid4())
        self.correlation_ids.add(correlation_id)
        self.sending_channel.basic_publish(
            exchange="exam_exchange",
            routing_key=message.examination_type,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=correlation_id,
                type="message",
            ),
            body=message.to_json(),
        )

        self.sending_channel.basic_publish(
            exchange="admin_exchange",
            routing_key=message.examination_type,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=correlation_id,
                type="message",
            ),
            body=message.to_json(),
        )
