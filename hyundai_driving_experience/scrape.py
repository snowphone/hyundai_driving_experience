from __future__ import annotations

from argparse import (
    ArgumentParser,
    Namespace,
)
from typing import Iterable

from bs4 import BeautifulSoup
from requests import post
from requests_html import (
    HTML,
    HTMLResponse,
    HTMLSession,
)

from hyundai_driving_experience.model import History


def load_page() -> HTMLResponse:
    sess = HTMLSession()

    resp: HTMLResponse = sess.get(  # type: ignore
        "https://drivingexperience.hyundai.co.kr/kr/scheduleEvent/gallery/board/list?pageIndex=1&detailsKey=&ctgry=&ctgry2=&f=&q="  # noqa: E501
    )
    resp.html.render()

    return resp


def get_schedules(html: HTML) -> set[str]:
    soup = BeautifulSoup(html.html, features="lxml")
    raw_strings: list[str] = [
        it.text for it in soup.find_all("div", {"class": "txt-area"})
    ]

    return {it.strip().replace("\n", " ") for it in raw_strings}


def notify(texts: Iterable[str], verbose: bool = False):
    data = "\n".join(texts).encode("utf-8")
    if verbose:
        print(f"Data: {data}")
    resp = post(
        "https://ntfy.sixtyfive.me/hyundai_driving_experience",
        data=data,
    )
    if verbose:
        print(f"{resp.ok=}, {resp.text=}")
    return


def main(args: Namespace):
    resp = load_page()

    entries = get_schedules(resp.html)

    latest = History.get_latest()

    diff = entries - latest

    data = diff if diff else ["No events found"]
    if args.verbose:
        print(*data, sep="\n")
    if args.notify:
        notify(data, args.verbose)

    History.store(entries)

    return


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--notify", action="store_true")
    parser.add_argument("--verbose", action="store_true")

    main(parser.parse_args())
