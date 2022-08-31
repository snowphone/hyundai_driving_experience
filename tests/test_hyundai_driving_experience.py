from hyundai_driving_experience import __version__
from hyundai_driving_experience.scrape import (
    get_schedules,
    load_page,
)


def test_version():
    assert __version__ == '0.1.0'


def test_get_schedules():

    expected = {
        "HMG 드라이빙 익스피리언스 센터 런칭 이벤트 2022.08.01",
        "2022년 HMG 드라이빙 익스피리언스 9월 프로그램 일정 2022.08.01",
    }
    assert expected <= get_schedules(load_page().html)
