import threading
import uuid

import pika
from actors import Actor
from utils.admin_payload import AdminPayload
from utils.payload_types import parse_payload


class Admin(Actor):
    def __init__(self) -> None:
        super().__init__()

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

    def _listen_for_results(self) -> None:
        def callback(ch, method, props, body):
            payload = parse_payload(props.type, body.decode())
            print(f"\nCorrelationId: {props.correlation_id}")
            payload.print_colored()
            ch.basic_ack(delivery_tag=method.delivery_tag)

        self.listening_channel.basic_consume(
            queue=self.queue, on_message_callback=callback, auto_ack=False
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

                message = AdminPayload(self.id, raw_input)
                self._send_message(message)

            except KeyboardInterrupt:
                break

    def _initialize_queues(self) -> None:
        self.id = "admin_" + self.id
        self.queue = self.id + "_queue"

        self.listening_channel.queue_declare(queue=self.queue, exclusive=True)
        self.listening_channel.queue_bind(
            exchange="admin_exchange",
            queue=self.queue,
        )

    def _send_message(self, payload: AdminPayload) -> None:
        self.sending_channel.basic_publish(
            exchange="admin_announcement_exchange",
            routing_key="",
            properties=pika.BasicProperties(
                correlation_id=str(uuid.uuid4()),
                type="admin",
            ),
            body=payload.to_json(),
        )
