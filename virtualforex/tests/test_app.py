import pytest
import pandas as pd

from virtualforex.core.data.pricedata import PriceData
from virtualforex.core.data.pricedatawindow import PriceDataWindow
from virtualforex.core.trading.buystoplosscalculator import BuyStopLossCalculator
from virtualforex.core.trading.sellstoplosscalculator import SellStopLossCalculator
from virtualforex.core.data.bar import Bar

FILE_PATH = "G:\\My Drive\\data\\MetaTrader5\\EURUSD_D1_cleaned.csv"


@pytest.fixture(scope='session')
def price_data():
    df = pd.read_csv(FILE_PATH, parse_dates=['Date'], date_format='%Y.%m.%d')
    df = df.set_index('Date', inplace=False)
    price_data = PriceData(df, 'EURUSD', 'D1')
    return price_data


@pytest.fixture(scope='session')
def page_size():
    return 100


def test_pricedatawindow(price_data, page_size):
    price_data_window = PriceDataWindow(price_data)
    last_bar = price_data_window.last_bar()
    price_data_window.last_page(page_size)
    assert last_bar == price_data_window.last_bar()
    assert len(price_data_window.first_page(page_size)) == page_size
    assert len(price_data_window.next_page(page_size)) == page_size
    assert len(price_data_window.prev_page(page_size)) == page_size
    assert len(price_data_window.last_page(page_size)) == page_size
    assert last_bar == price_data_window.last_bar()
    assert len(price_data_window.current_page()) == page_size


def test_bar():
    bar = Bar(None, open=2, high=4, low=1, close=3)
    assert bar.range() == 3
    assert bar.body_range() == 1


def test_buystoplosscalculator():
    calculator = BuyStopLossCalculator(1000, 10000, 0.02, 0.0001)
    stop_loss = calculator.calculate(1.15)
    assert 1.1476 < stop_loss < 1.1478

def test_sellstoplosscalculator():
    calculator = SellStopLossCalculator(1000, 10000, 0.02, 0.0001)
    stop_loss = calculator.calculate(1.15)
    assert 1.1521 < stop_loss < 1.1523