import enum

from utils.admin_payload import AdminPayload
from utils.message_payload import MessagePayload


class PayloadType(enum.StrEnum):
    ADMIN = enum.auto()
    MESSAGE = enum.auto()


def parse_payload(payload_type: str, payload: str) -> AdminPayload | MessagePayload:
    match payload_type:
        case PayloadType.ADMIN:
            return AdminPayload.from_json(payload)
        case PayloadType.MESSAGE:
            return MessagePayload.from_json(payload)
        case _:
            raise TypeError("Unsupported payload type")
