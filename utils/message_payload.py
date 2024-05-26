import dataclasses
import json
from typing import Optional
import json

from colorama import Fore

from utils import BaseDC
from utils.examination_types import (
    ExaminationStatus,
    ExaminationType,
    map_to_examination_type,
)


@dataclasses.dataclass
class MessagePayload(BaseDC):
    source: str
    patient: str
    examination_type: ExaminationType
    status: ExaminationStatus

    @classmethod
    def parse_messages_payload(
        cls, source: str, raw_input: str
    ) -> Optional["MessagePayload"]:
        parsed_input = raw_input.strip().split(" ")
        if len(parsed_input) < 2:
            return None

        raw_examination_type, patient = parsed_input[0], parsed_input[1]
        if examination_type := map_to_examination_type(raw_examination_type):
            return MessagePayload(
                source=source,
                patient=patient,
                examination_type=examination_type,
                status=ExaminationStatus.IN_PROGRESS,
            )
        return None

    def get_color(self) -> str:
        return Fore.CYAN

    def __str__(self):
        def _display_dict(d: dict[str, str]):
            return "\n\t".join(f"{key.upper()} : {value}" for key, value in d.items())

        return f"MESSAGE:\n\t{_display_dict(dataclasses.asdict(self))}"
