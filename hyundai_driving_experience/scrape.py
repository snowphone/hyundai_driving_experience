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


def notify(texts: Iterable[str]):
    data = "\n".join(texts).encode("utf-8")
    post(
        "https://ntfy.sixtyfive.me/hyundai_driving_experience",
        data=data,
    )
    return


def main(args: Namespace):
    resp = load_page()

    entries = get_schedules(resp.html)

    latest = History.get_latest()

    diff = entries - latest

    if diff:
        print(*diff, sep="\n")
        if args.notify:
            notify(diff)

    History.store(entries)

    return


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--notify", action="store_true")

    main(parser.parse_args())
