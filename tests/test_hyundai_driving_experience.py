from hyundai_driving_experience import __version__
from hyundai_driving_experience.scrape import (
    get_schedules,
    load_page,
)


def test_version():
    assert __version__ == "0.1.0"


def test_get_schedules():
    expected = {
        "2023년 HMG 드라이빙 익스피리언스 5월 운영 공지 2023.04.10",
        "2023년 HMG 드라이빙 익스피리언스 6월 운영 공지 2023.05.01",
    }
    assert expected <= get_schedules(load_page().html)
