import requests_html
from bs4 import BeautifulSoup


def main():
    sess = requests_html.HTMLSession()

    resp = sess.get(
        "https://drivingexperience.hyundai.co.kr/kr/scheduleEvent/gallery/board/list?pageIndex=1&detailsKey=&ctgry=&ctgry2=&f=&q="  # noqa: E501
    )
    resp.html.render()

    soup = BeautifulSoup(resp.html.html, features="lxml")

    # print(soup.find_all("a", {"class": "img-wrap"}))
    print(
        *[
            it.text.strip().split('\n')[0]
            for it in soup.find_all("div", {"class": "txt-area"})
        ],
        sep='\n'
    )

    return


if __name__ == "__main__":
    main()
