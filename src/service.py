import asyncio
from collections import defaultdict
from datetime import datetime, timedelta, date
from typing import Iterable

from src.domain.page_provider import OKXPageProvider
from src.domain.parser import OKXParser
from src.dto import NewsRequest, NewsHeadline, PageHeadlines, NewsRecord
from src.infrastructure.logger import logger


class OKXScrapingService:

    def __init__(self):
        self.parser = OKXParser()
        self.page_provider = OKXPageProvider()
        self._headline_storage: dict[date, set[NewsHeadline]] = defaultdict(set)
        self._record_storage: list[NewsRecord] = []

    async def get_news_by_period(self, request: NewsRequest) -> Iterable[NewsRecord]:
        main_page_content = await self.page_provider.get_main_page()
        qty = self.parser.get_pages_qty(main_page_content)
        if request.end_date == datetime.now().date:
            newest_page = 1
            oldest_page = await self._bsearch_date_page(start=1, end=qty, searching_date=request.start_date)
        else:
            oldest_page, newest_page = await asyncio.gather(
                self._bsearch_date_page(start=1, end=qty, searching_date=request.start_date),
                self._bsearch_date_page(start=1, end=qty, searching_date=request.end_date),
            )
        oldest_page, newest_page = await asyncio.gather(
            self._ensure_oldest_date_page(oldest_page, pages_qty=qty, start_date=request.start_date),
            self._ensure_newest_date_page(newest_page, end_date=request.end_date),
        )
        await asyncio.gather(
            *[self._scrape_headline_page_by_num(i) for i in range(newest_page, oldest_page + 1)]
        )
        await asyncio.gather(
            *[self._scrape_news_record(r)
              for r in self._get_filtered_headlines_by_period(request.start_date, request.end_date)]
        )
        return self._record_storage

    async def _scrape_headline_page_by_num(self, num: int) -> PageHeadlines:
        page_content = await self.page_provider.get_page_by_number(num)
        page_records =  PageHeadlines(num, self.parser.extract_headlines_from_page(page_content))
        self._put_to_storage(page_records)
        logger.debug(f'parsed headline {PageHeadlines!r}')
        return page_records

    async def _scrape_news_record(self, news_headline: NewsHeadline) -> None:
        page_content = await self.page_provider.get_news_page_by_url(news_headline.body_url)
        news_record_body =  self.parser.extract_news_body_from_page(page_content)
        self._record_storage.append(
            NewsRecord(
                date=news_headline.date,
                title=news_headline.title,
                body=news_record_body,
            )
        )

    async def _bsearch_date_page(self, start: int, end: int, searching_date: date) -> int:
        """
        :param start: newest articles page
        :param end: oldest news
        :param searching_date: desired news date
        :return: number of page which contains searching_date or last page number if no desired date was found

        to decrease loading time make aggressive binary search:
            load pages for middle,
            right_middle (middle of the first half),
            right_middle (middle of the second half),
        """
        if end - start < 0:
            return start
        if end - start < 4:
            searching_pages = range(start, end + 1)
        else:
            # divide the range into 3 parts
            searching_pages = [
                round(x)
                for x in ((end - start) / 3, (end - start) / 2, 2 * (end - start) / 3)
            ]

        page_records: list[PageHeadlines] = await asyncio.gather(
            *[
                self._scrape_headline_page_by_num(num) for num in searching_pages
            ]
        )
        left = start
        for page_headlines in page_records:
            if searching_date == page_headlines:
                return page_headlines.page_num
            elif searching_date > page_headlines:
                return await self._bsearch_date_page(left, page_headlines.page_num - 1, searching_date)
            left = page_headlines.page_num
        return await self._bsearch_date_page(left + 1, end, searching_date)

    async def _ensure_oldest_date_page(self, page_num: int, pages_qty: int, start_date: date) -> int:
        if page_num == pages_qty:
            return page_num
        pages_qty += 1
        is_start_date_on_page = True
        while is_start_date_on_page and page_num <= pages_qty:
            records = await self._scrape_headline_page_by_num(page_num)
            is_start_date_on_page = start_date == records
            page_num += 1
        return page_num

    async def _ensure_newest_date_page(self, page_num: int, end_date: date) -> int:
        if page_num <= 1:
            return page_num
        is_start_date_on_page = True
        while is_start_date_on_page and page_num >= 1:
            page_num -= 1
            records = await self._scrape_headline_page_by_num(page_num)
            is_start_date_on_page = end_date in records
        return page_num + 1

    def _put_to_storage(self, page_records:PageHeadlines):
        for r in page_records.records:
            self._headline_storage[r.date].add(r)

    def _get_filtered_headlines_by_period(self, start_date: date, end_date: date) -> Iterable[NewsHeadline]:
        results = []
        for delta in range((end_date - start_date).days + 1):
            results.extend(self._headline_storage[start_date + timedelta(delta)])
        return results
