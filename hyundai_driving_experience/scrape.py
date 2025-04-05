from __future__ import annotations

import logging
import os
import sys
from argparse import (
    ArgumentParser,
    Namespace,
)
from operator import attrgetter
from typing import Iterable

from bs4 import BeautifulSoup
from requests import post
from requests_html import (
    HTML,
    HTMLResponse,
    HTMLSession,
)

from hyundai_driving_experience.model import History

log_level = attrgetter(os.environ.get("LOG_LEVEL", "INFO").upper())(logging)


logging.basicConfig(
    stream=sys.stderr,
    level=log_level,
    format=(
        "[%(levelname).1s %(asctime)s.%(msecs)03d+09:00 "
        "%(processName)s:%(filename)s:%(funcName)s:"
        "%(module)s:%(lineno)d]\n"
        "%(message)s"
    ),
    datefmt="%Y-%m-%dT%H:%M:%S",
)

logger = logging.getLogger()


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
        it.text for it in soup.find_all("div", {"class": "txt"})
    ]
    logger.info(f"Fetched data: {raw_strings}")

    return {it.strip().replace("\n", " ") for it in raw_strings}


def notify(texts: Iterable[str], verbose: bool = False):
    data = "\n".join(texts).encode("utf-8")

    logger.info(f"Data to notify: {data}")
    if verbose:
        print(f"Data: {data}")

    resp = post(
        "https://ntfy.sixtyfive.me/hyundai_driving_experience",
        data=data,
    )

    logger.info(f"{resp.ok=}, {resp.text=}")
    if verbose:
        print(f"{resp.ok=}, {resp.text=}")

    return


def main(args: Namespace):
    resp = load_page()

    entries = get_schedules(resp.html)

    latest = History.get_latest()
    logger.info(f"{latest=}")

    diff = entries - latest
    logger.info(f"{diff=}")

    DNE = ["No events found"]

    data = diff if diff else DNE
    if args.verbose:
        print(*data, sep="\n")
    if args.notify and data != DNE:
        notify(data, args.verbose)
    else:
        logger.info("Since there has been no news, no notification will be sent.")

    History.store(entries)

    return


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--notify", action="store_true")
    parser.add_argument("--verbose", action="store_true")

    main(parser.parse_args())
