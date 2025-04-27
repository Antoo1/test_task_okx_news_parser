from datetime import date
import os
import pytest

from src.domain.parser import OKXParser
from src.dto import NewsHeadline


CURRENT_DIR = os.path.dirname(__file__)


@pytest.fixture
def fake_page_content() -> str:
    with open(f'{CURRENT_DIR}/test_data.html', 'r') as f:
        return f.read()


class TestGetPagesQty:

    def test_success(self, fake_page_content):
        actual = OKXParser().get_pages_qty(fake_page_content)

        assert actual == 143


class TestExtractNewsFromPage:

    def test_success(self, fake_page_content):
        expected_result = [
            NewsHeadline(title='OKX to\n'
                                '                                    adjust tick size of '
                                'spot, margin, and perpetual futures\n'
                                '                                ',
                         date=date(2025, 4, 17),
                         body_url='/help/okx-to-adjust-tick-size-for-some-spot-trading-pairs-apr-17-2025'),
            NewsHeadline(title='OKX to\n'
                                '                                    postpone adjusting '
                                'margin position tiers for USDT\n'
                                '                                ',
                         date=date(2025, 4, 16),
                         body_url='/help/okx-to-postpone-adjusting-margin-position-tiers-for-usdt'),
            NewsHeadline(title='OKX to\n'
                                '                                    adjust discount rate '
                                'tiers for multiple tokens\n'
                                '                                ',
                         date=date(2025, 4, 15),
                         body_url='/help/okx-to-adjust-discount-rate-tiers-for-multiple-tokens-20250415'),
            NewsHeadline(title='OKX to\n'
                                '                                    list perpetual for '
                                'WCT crypto, along with its margin trading\n'
                                '                                    and Simple Earn\n'
                                '                                ',
                         date=date(2025, 4, 15),
                         body_url='/help/okx-to-list-perpetual-for-wct-crypto-along-with-its-margin-trading-and'),
            NewsHeadline(title='\n'
                                '                                    Announcement on the '
                                'Price Volatility of MANTRA (OM)\n'
                                '                                ',
                         date=date(2025, 4, 14),
                         body_url='/help/announcement-on-the-price-volatility-of-mantra-om'),
            NewsHeadline(title='OKX will\n'
                                '                                    launch WCT/USDT for '
                                'spot trading\n'
                                '                                ',
                         date=date(2025, 4, 14),
                         body_url='/help/okx-will-launch-wct-usdt-for-spot-trading'),
            NewsHeadline(title='OKX to\n'
                                '                                    adjust margin '
                                'position tiers and discount rates for ETH, BETH,\n'
                                '                                    STETH\n'
                                '                                ',
                         date=date(2025, 4, 12),
                         body_url='/help/okx-to-adjust-margin-position-tiers-and-discount-rates-for-usdt-eth-beth'),
            NewsHeadline(title='OKX to\n'
                                '                                    adjust position '
                                'tiers of several futures\n'
                                '                                ',
                         date=date(2025, 4, 11),
                         body_url='/help/okx-to-adjust-position-tiers-of-several-futures-20250411'),
            NewsHeadline(title='OKX to\n'
                                '                                    adjust funding rate '
                                'interval for PROMPTUSDT perpetual futures\n'
                                '                                ',
                         date=date(2025, 4, 11),
                         body_url='/help/ann-okx-to-adjust-funding-rate-interval-for-certain-perpetual-futures-250411'),
            NewsHeadline(title='OKX to\n'
                                '                                    list perpetual for '
                                'PROMPT crypto, along with its margin trading\n'
                                '                                    and Simple Earn\n'
                                '                                ',
                         date=date(2025, 4, 10),
                         body_url='/help/okx-to-list-perpetual-for-prompt-crypto-along-with-its-margin-trading-and'),
            NewsHeadline(title='OKX to\n'
                                '                                    list perpetual for '
                                'BABY crypto, along with its margin trading\n'
                                '                                    and Simple Earn\n'
                                '                                ',
                         date=date(2025, 4, 10),
                         body_url='/help/okx-to-list-perpetual-for-baby-crypto-along-with-its-margin-trading-and'),
            NewsHeadline(title='OKX to\n'
                                '                                    adjust funding rate '
                                'interval for GASUSDT perpetual futures\n'
                                '                                ',
                         date=date(2025, 4, 10),
                         body_url='/help/ann-okx-to-adjust-funding-rate-interval-for-certain-perpetual-futures-250410'),
            NewsHeadline(title='OKX\n'
                                '                                    Wallet to upgrade '
                                'the services for Fractal Bitcoin BRC-20\n'
                                '                                ',
                         date=date(2025, 4, 10),
                         body_url='/help/okx-wallet-to-upgrade-the-services-for-fractal-bitcoin-brc-20'),
            NewsHeadline(title='OKX to\n'
                                '                                    list BABY (Babylon) '
                                'for spot trading and deliver pre-market\n'
                                '                                    futures for BABY '
                                'crypto\n'
                                '                                ',
                         date=date(2025, 4, 9),
                         body_url='/help/okx-to-list-baby-babylon-for-spot-trading-and-deliver-pre-market-futures-for'),
            NewsHeadline(title='OKX\n'
                                '                                    Wallet to Launch '
                                'Cryptopedia Season 32\n'
                                '                                ',
                         date=date(2025, 4, 9),
                         body_url='/help/okx-wallet-to-launch-cryptopedia-season-32')]

        actual = OKXParser().extract_headlines_from_page(fake_page_content)

        assert actual == expected_result
