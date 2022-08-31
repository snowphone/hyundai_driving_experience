from hyundai_driving_experience.model import History


def test_empty_db():
    assert History.get_latest() == set()


def test_store_and_load():
    data = {
        "HMG 드라이빙 익스피리언스 센터 런칭 이벤트 2022.08.01",
        "2022년 HMG 드라이빙 익스피리언스 9월 프로그램 일정 2022.08.01",
    }
    History.store(data)

    assert History.get_latest() == data
