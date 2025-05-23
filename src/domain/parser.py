import re
from datetime import date, datetime

from bs4 import BeautifulSoup

from src.dto import NewsHeadline


class OKXParser:
    _article_class = re.compile(r'\bindex_articleItem_')
    _article_title_class = re.compile(r'\bindex_articleTitle_')
    _article_date_class = re.compile(r'\bindex_detailsRow_')
    _date_regext = re.compile(r'(?<=ublished\son\s).*$')
    _article_body_class = re.compile(r'\bindex_richTextContent_')


    def get_pages_qty(self, page_content: str) -> int:
        soup = BeautifulSoup(page_content, 'html.parser')
        links = soup.find_all('a', class_='okui-pagination-item')
        return int(links[-1].text)

    def extract_headlines_from_page(self, page_content: str) -> list[NewsHeadline]:
        result = []
        soup = BeautifulSoup(page_content, 'html.parser')
        news_list = soup.find_all('li', class_=self._article_class)
        for row in news_list:
            title = row.find('div', class_=self._article_title_class).text
            url = row.find('a').get('href')
            news_date = row.find('div', class_=self._article_date_class).text
            news_date = self._date_regext.search(news_date).group(0)
            result.append(NewsHeadline(title=title, date=_parse_date(news_date), body_url=url))
        return result

    def extract_news_body_from_page(self, page_content: str) -> str:
        soup = BeautifulSoup(page_content, 'html.parser')
        news_body = soup.find('div', class_=self._article_body_class)
        return news_body.decode_contents()


def _parse_date(date_str: str) -> date:
    return datetime.strptime(date_str, "%b %d, %Y").date()
