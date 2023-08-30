# analyze.py
import json
from pathlib import Path

current_dir = Path(__file__).parent


def get_foreign_data():
    # 'address' key still exists
    with open(current_dir / "new_foreign_response.json", "r") as f:
        data = json.load(f)

    return data


def analyze(data):
    # Well it still works, but if analyze data requires data with addresses
    # for its gargantuan further processing
    # it makes sense to give it data with addresses. This will prevent us
    # from the loop of reminiscing as to why data is like that
    send_adds_to = [d["addresses"][0] for d in data]
    return send_adds_to


def send_advertisements(send_adds_to, msg="Algorithm is real, you are in Matrix!"):
    for home in send_adds_to:
        print(f"Sent mail to : {home} , Msg: {msg}")


def main():
    foreign_data = get_foreign_data()
    foreign_data = [d for d in foreign_data if len(d["addresses"]) > 0]
    send_advertisements_to = analyze(data=foreign_data)
    send_advertisements(send_adds_to=send_advertisements_to, msg="Keep Working")
