import json
from pathlib import Path

from demo.new_approach.models import PersonDetails, Address

current_path: Path = Path(__file__)


# Loaders should be separate
def load_foreign_data() -> tuple[PersonDetails, ...]:

    with open(current_path.parent.parent / "foreign_response.json", "r") as f:
        data = json.load(f)

    return tuple([PersonDetails.model_validate(d) for d in data])


def analyze(data: tuple[PersonDetails, ...]) -> tuple[Address, ...]:
    return tuple([d.addresses[0] for d in data])


def send_advertisements(
    send_adds_to: tuple[Address, ...],
    msg: str = "Algorithm is real, you are in Matrix!",
):
    for address in send_adds_to:
        print(f"Sent mail to {address}, MSG: {msg}")


def main() -> None:
    foreign_data: tuple[PersonDetails, ...] = load_foreign_data()
    send_advertisements(
        send_adds_to=analyze(data=foreign_data),
        msg="Keep Working!",
    )
