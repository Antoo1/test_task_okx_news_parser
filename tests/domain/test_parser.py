from datetime import date
import os
import pytest

from src.domain.parser import OKXParser
from src.dto import NewsHeadline


CURRENT_DIR = os.path.dirname(__file__)


@pytest.fixture
def fake_headlines_page_content() -> str:
    with open(f'{CURRENT_DIR}/test_headlines_data.html', 'r') as f:
        return f.read()


@pytest.fixture
def fake_news_body_page_content() -> str:
    with open(f'{CURRENT_DIR}/test_body.html', 'r') as f:
        return f.read()


class TestGetPagesQty:

    def test_success(self, fake_headlines_page_content):
        actual = OKXParser().get_pages_qty(fake_headlines_page_content)

        assert actual == 143


class TestExtractHeadlinesFromPage:

    def test_success(self, fake_headlines_page_content):
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

        actual = OKXParser().extract_headlines_from_page(fake_headlines_page_content)

        assert actual == expected_result


class TestExtractNewsBodyFromPage:

    def test_success(self, fake_news_body_page_content):
        expected = '<p>We are pleased to announce that USDT-margined perpetual futures for INIT will be enabled at 11:30 am UTC on April 24, 2025. The updates will cover both the web and app interfaces as well as the API. The details are as follows:</p><p><br/><b>I. Listing schedule</b></p><ul><li><p>INIT/USDT perpetual futures trading will open at 11:30 am UTC on April 24, 2025.</p></li></ul><p><br/><b>II. Perpetual futures trading</b></p><p><b>INIT perpetual futures:</b></p><p>Initia is an L1 blockchain that unites appchains to unlock their full value through interwoven infrastructure and aligned economics.</p><ul><li><p>Asset name: Initia</p></li><li><p>Ticker: INIT</p></li><li><p>Website：<a class="okui-powerLink-a11y" href="https://initia.xyz/" rel="noopener" target="_blank">https://initia.xyz/</a></p></li><li><p>Official X: <a class="okui-powerLink-a11y" href="https://x.com/initia" rel="noopener" target="_blank">https://x.com/initia</a></p></li></ul><div class="table-wrap"><table><tbody><tr><td><p><b>Features</b></p></td><td><p><b>Details</b></p></td></tr><tr><td><p>Underlying</p></td><td><p>INIT/USDT index</p></td></tr><tr><td><p>Settlement crypto</p></td><td><p>USDT</p></td></tr><tr><td><p>Face value</p></td><td><p>10</p></td></tr><tr><td><p>Price quotation</p></td><td><p>1 INIT value calculated in USDT equivalent</p></td></tr><tr><td><p>Tick size</p></td><td><p>0.0001</p></td></tr><tr><td><p>Leverage</p></td><td><p>0.01-20x</p></td></tr><tr><td><p>Funding rate</p></td><td><p>clamp [Average premium index + clamp (Interest rate – Average premium index, 0.05%, -0.05%), 1.50%, -1.50%]</p><p>For average premium index and interest rate calculations, refer to our <a class="okui-powerLink-a11y" href="/help/iv-introduction-to-perpetual-swap-funding-fee" rel="noopener">product documentation</a></p></td></tr><tr><td><p>Funding fee settlement interval</p></td><td><p>4 hours</p></td></tr><tr><td><p>Trading hours</p></td><td><p>24/7</p></td></tr></tbody></table></div><p>Note: To avoid unreasonable fees arising from significant premium fluctuations of a newly launched contract, the upper limit of the funding fee before 4:00 pm UTC on April 24, 2025 is 0.5%. After 4:00 pm UTC on April 24, 2025, the upper limit of the predicted funding fee will be adjusted back to the regular rate of 1.5%. (The funding fee for this period will be charged at 8:00 pm UTC on April 24, 2025.) <b>If there is a deviation from the contract price, the funding fee limit will be adjusted according to market conditions.</b></p><p><br/>The price limit rules of INIT USDT-margined perpetual futures trading are the same as those of other currencies. Please refer to our perpetual futures trading guides for further details.</p><p><br/>USDT-margined perpetual futures trading: <a class="okui-powerLink-a11y" href="/help/okx-perpetual-swap-trading-user-agreement" rel="noopener">OKX Perpetual Futures Trading User Agreement</a></p><p><br/>OKX team</p><p>April 24, 2025<br/></p>'

        actual = OKXParser().extract_news_body_from_page(fake_news_body_page_content)

        assert actual == expected
