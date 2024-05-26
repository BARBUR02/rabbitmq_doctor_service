from actors.admin import Admin
from actors.doctor import Doctor
from actors.technician import Technician
from utils.examination_types import ExaminationType
from utils.actor_register_parser import get_examination_types, parse_parameters


def main() -> None:
    args = parse_parameters()
    match args.actor:
        case "doctor":
            actor = Doctor()
        case "technician":
            actor = Technician(get_examination_types())
        case "admin":
            actor = Admin()

    actor.run()


if __name__ == "__main__":
    main()
