import pytest
from bs4 import BeautifulSoup
from requests_html import HTML

from hyundai_driving_experience.scrape import get_schedules


@pytest.fixture
def sample_html():
    html_content = """
    <html>
        <body>
            <div class="txt">Event 1 Details</div>
            <div class="txt">Event 2</div>
            <div class="other">Not an event</div>
            <div class="txt"> Event 3 More details
            </div>
        </body>
    </html>
    """.strip()
    return HTML(html=html_content)


def test_get_schedules(sample_html):
    # When
    result = get_schedules(sample_html)

    # Then
    expected = {
        "Event 1 Details",
        "Event 2",
        "Event 3 More details"
    }
    assert result == expected


def test_get_schedules_empty():
    # Given
    empty_html = HTML(html="<html><body></body></html>")

    # When
    result = get_schedules(empty_html)

    # Then
    assert result == set()