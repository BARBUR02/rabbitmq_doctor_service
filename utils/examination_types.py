import enum
from typing import Optional


class ExaminationType(enum.StrEnum):
    KNEE = enum.auto()
    HEAP = enum.auto()
    LEG = enum.auto()
    HEAD = enum.auto()

    def to_queue_name(self) -> str:
        return f"{self}_queue"


class ExaminationStatus(enum.StrEnum):
    IN_PROGRESS = enum.auto()
    DONE = enum.auto()


def map_to_examination_type(value: str) -> Optional[ExaminationType]:
    match (value.strip().lower()):
        case "knee":
            return ExaminationType.KNEE
        case "heap":
            return ExaminationType.HEAP
        case "leg":
            return ExaminationType.LEG
        case "head":
            return ExaminationType.HEAD
        case _:
            return None
