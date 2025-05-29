from datetime import date, time
from typing import override

from requests import Response, post
from src.core.datetime_utils import date2str, unix, date2datetime
from src.data.data_source.data_source import DataSource


class PHD2025DataSource(DataSource):
    def __init__(self, phd_program_url: str):
        self.url = phd_program_url

    @override
    def fetch(self, day: date, page: int) -> str:
        response: Response = post(
            self.url,
            params={"date": date2str(day)},
            headers={
                "Next-Action": "82ca8b1f3117919c996153175a1ea160dc36115a",
                "Accept": "text/x-component"
            },
            json=[{
                "locale": "ru",
                "page": page,
                "tagSlugs": [],
                "startDateFrom": unix(date2datetime(day, time(hour=0, minute=0, second=0))),
                "startDateTo": unix(date2datetime(day, time(hour=23, minute=59, second=59))),
                "eventType": "forum",
                "hidePast": False,
                "locationId": 0,
                "talkIds": []
            }]
        )
        response.raise_for_status()
        return response.text
