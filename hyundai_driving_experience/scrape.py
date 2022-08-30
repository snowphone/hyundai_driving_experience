from __future__ import annotations

from bs4 import BeautifulSoup
from requests_html import (
    HTML,
    HTMLResponse,
    HTMLSession,
)


def load_page() -> HTMLResponse:
    sess = HTMLSession()

    resp: HTMLResponse = sess.get(  # type: ignore
        "https://drivingexperience.hyundai.co.kr/kr/scheduleEvent/gallery/board/list?pageIndex=1&detailsKey=&ctgry=&ctgry2=&f=&q="  # noqa: E501
    )
    resp.html.render()

    return resp


def get_schedules(html: HTML):
    soup = BeautifulSoup(html.html, features="lxml")
    raw_strings: list[str] = [
        it.text for it in soup.find_all("div", {"class": "txt-area"})
    ]

    return [it.strip().replace("\n", " ") for it in raw_strings]


def main():
    resp = load_page()

    entries = get_schedules(resp.html)

    print(*entries, sep='\n')

    return


if __name__ == "__main__":
    main()
