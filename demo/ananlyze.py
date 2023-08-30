# analyze.py
import json
from pathlib import Path

current_dir = Path(__file__).parent


def get_foreign_data():
    # 'address' key still exists
    with open(current_dir / "mou.json", "r") as f:
        data = json.load(f)

    return data


def analyze(data):
    send_adds_to = [d["email_addresses"][0] for d in data]
    return send_adds_to


def send_advertisements(send_adds_to, msg="Algorithm is real, you are in Matrix!"):
    for home in send_adds_to:
        print(f"Sent e-mail to : {home} , Msg: {msg}")


def main():
    foreign_data = get_foreign_data()
    send_advertisements_to = analyze(data=foreign_data)
    send_advertisements(send_adds_to=send_advertisements_to, msg="Keep Working")
