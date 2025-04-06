from hyundai_driving_experience import __version__
from hyundai_driving_experience.scrape import (
    get_schedules,
    load_page,
)


def test_version():
    assert __version__ == "0.1.0"
