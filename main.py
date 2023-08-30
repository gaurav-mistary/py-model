import datetime
import time
import zoneinfo

import click
from demo.ananlyze import main as analyze_main
from demo.new_approach.analyze import main as new_approach_main


@click.group(name="demo")
def demo():
    pass


@demo.command(help="Application analyze department")
def analyze():
    analyze_main()


@demo.command(help="Run this!!")
def runner():
    utc = zoneinfo.ZoneInfo("UTC")

    start = datetime.datetime.now(tz=utc)

    while (atd := datetime.datetime.now(tz=utc) - start).seconds < 8:
        print(f"[+] {atd.seconds} seconds passed. All is good ...")
        time.sleep(1)

        if atd.seconds == 4:
            print(f"[+] It's {atd.seconds} past start. Analyze time ... ")
            analyze_main()
            print(f"[+] Done Analyzing ...")


@demo.command(help="New approach to runner")
def new_runner():
    utc = zoneinfo.ZoneInfo("UTC")

    start = datetime.datetime.now(tz=utc)

    while (atd := datetime.datetime.now(tz=utc) - start).seconds < 8:
        print(f"[+] {atd.seconds} seconds passed. All is good ...")
        time.sleep(1)

        if atd.seconds == 4:
            print(f"[+] It's {atd.seconds} past start. Analyze time ... ")
            new_approach_main()
            print(f"[+] Done Analyzing ...")


if __name__ == "__main__":
    demo()
