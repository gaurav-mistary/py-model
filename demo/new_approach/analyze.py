import json
from pathlib import Path

from demo.new_approach.models import PersonDetails, Address, PersonDetailsWithoutAddress

current_path: Path = Path(__file__)


# Loaders should be separate
def load_foreign_data() -> tuple[PersonDetailsWithoutAddress, ...]:

    # The moment you change this to 'new_foreign_response' it'll break
    # coz the PersonDetails object has validators while constructing
    with open(current_path.parent.parent / "new_foreign_response.json", "r") as f:
        data = json.load(f)

    return tuple([PersonDetailsWithoutAddress.model_validate(d) for d in data])


def analyze(data: tuple[PersonDetailsWithoutAddress, ...]) -> tuple[Address, ...]:
    return tuple([d.addresses[0] for d in data])


def send_advertisements(
    send_adds_to: tuple[Address, ...],
    msg: str = "Algorithm is real, you are in Matrix!",
):
    for address in send_adds_to:
        print(f"Sent mail to {address}, MSG: {msg}")


def main() -> None:
    # foreign_data: tuple[PersonDetailsWithoutAddress, ...] = load_foreign_data()
    send_advertisements(
        send_adds_to=analyze(data=()),
        msg="Keep Working!",
    )
