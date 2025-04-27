from dataclasses import dataclass
from datetime import date
from typing import Iterable


@dataclass
class NewsRequest:
    start_date: date
    end_date: date


@dataclass
class NewsHeadline:
    title: str
    date: date
    body_url: str

    def __hash__(self):
        return hash((self.date, self.title))


@dataclass
class NewsRecord:
    title: str
    date: date
    body: str

    def __hash__(self):
        return hash((self.date, self.title))


@dataclass
class PageHeadlines:
    page_num: int
    records: Iterable[NewsHeadline]

    def __lt__(self, other):
        return all(map(lambda r: r.date < other, self.records))

    def __gt__(self, other):
        return all(map(lambda r: r.date > other, self.records))

    def __eq__(self, other):
        return any(map(lambda r: r.date == other, self.records))
