from dataclasses import dataclass, asdict
import json
from typing import Type, TypeVar
from colorama import Fore, Style, init

T = TypeVar("T", bound="Base")

init(autoreset=True)


@dataclass
class BaseDC:
    def to_json(self) -> str:
        return json.dumps(asdict(self))

    @classmethod
    def from_json(cls: Type[T], json_string: str) -> T:
        return cls(**json.loads(json_string))

    def print_colored(self) -> None:
        color = self.get_color()
        print(f"{color}{self}{Style.RESET_ALL}")

    def get_color(self) -> str:
        return Style.RESET_ALL
