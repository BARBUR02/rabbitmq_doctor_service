import dataclasses

from colorama import Fore

from utils import BaseDC


@dataclasses.dataclass
class AdminPayload(BaseDC):
    source: str
    message: str

    def __str__(self):
        def _display_dict(d: dict[str, str]):
            return "\n\t".join(f"{key.upper()} : {value}" for key, value in d.items())

        return f"MESSAGE:\n\t{_display_dict(dataclasses.asdict(self))}"

    def get_color(self) -> str:
        return Fore.RED
