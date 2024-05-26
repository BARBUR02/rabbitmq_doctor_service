from abc import ABC, abstractmethod
import uuid

import pika


class Actor(ABC):
    def __init__(self) -> None:
        self.id = str(uuid.uuid4())
        self.listening_connection = pika.BlockingConnection(
            pika.ConnectionParameters("localhost")
        )
        self.sending_connection = pika.BlockingConnection(
            pika.ConnectionParameters("localhost")
        )
        self.listening_channel = self.listening_connection.channel()
        self.sending_channel = self.sending_connection.channel()
        self._initialize_queues()

    @abstractmethod
    def run(self) -> None:
        pass

    @abstractmethod
    def _initialize_queues(self) -> None:
        pass

    def _destruct(self) -> None:
        if self.sending_channel.is_open:
            self.sending_channel.close()
        if self.listening_channel.is_open:
            self.listening_channel.close()
        if self.listening_connection.is_open:
            self.listening_connection.close()
        if self.sending_connection.is_open:
            self.sending_connection.close()
