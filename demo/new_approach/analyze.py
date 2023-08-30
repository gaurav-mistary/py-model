import json
from pathlib import Path

from pydantic import EmailStr

from demo.new_approach.models import (
    PersonDetailsWithEmail,
)

current_path: Path = Path(__file__)


# Loaders should be separate
def load_foreign_data() -> tuple[PersonDetailsWithEmail, ...]:
    with open(current_path.parent.parent / "mou.json", "r") as f:
        data = json.load(f)

    return tuple([PersonDetailsWithEmail.model_validate(d) for d in data])


def analyze(data: tuple[PersonDetailsWithEmail, ...]) -> tuple[EmailStr, ...]:
    return tuple([d.email_addresses[0] for d in data])


def send_advertisements(
    send_adds_to: tuple[EmailStr, ...],
    msg: str = "Algorithm is real, you are in Matrix!",
):
    for address in send_adds_to:
        print(f"Sent e-mail to {address}, MSG: {msg}")


def main() -> None:
    foreign_data: tuple[PersonDetailsWithEmail, ...] = load_foreign_data()
    send_advertisements(
        send_adds_to=analyze(data=foreign_data),
        msg="Keep Working!",
    )
