import argparse

from utils.examination_types import ExaminationType


def parse_parameters() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Factory for registering  different actor types (doctor/administrator/technician) and their parameters"
    )

    parser.add_argument(
        "--actor",
        help="Requested actor type",
        type=str,
        required=True,
        choices=["admin", "doctor", "technician"],
    )

    return parser.parse_args()


def get_examination_types() -> list[ExaminationType]:
    examination_types = [exam_type for exam_type in ExaminationType]
    raw_examination_types = input(
        f"Provide supported examination types: [{' '.join(examination_types)}]: "
    ).split(" ")
    return [
        exam_type
        for exam_type in raw_examination_types
        if exam_type in examination_types
    ]
