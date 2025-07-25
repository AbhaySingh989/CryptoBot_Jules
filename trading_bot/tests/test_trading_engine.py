import pytest
from unittest.mock import MagicMock, patch
from trading_bot.core.trading_engine import TradingEngine
import pandas as pd

@pytest.fixture
def engine():
    with patch('importlib.import_module') as mock_import:
        with patch('trading_bot.core.api_client.CoinSwitchProApiClient') as mock_api_client:
            mock_strategy = MagicMock()
            mock_import.return_value = mock_strategy

            mock_api_client_instance = mock_api_client.return_value
            mock_api_client_instance.api_key = "test_key"
            mock_api_client_instance.api_secret = "0000000000000000000000000000000000000000000000000000000000000000"

            engine = TradingEngine()
            engine.strategy = mock_strategy
            engine.api_client = mock_api_client_instance
            return engine

def test_load_strategy(engine):
    assert engine.strategy is not None

def test_handle_websocket_message(engine):
    event = 'FETCH_CANDLESTICK_CS_PRO'
    data = {'s': 'BTCUSDT', 'o': 1, 'h': 2, 'l': 0.5, 'c': 1.5, 'v': 100, 't': 12345}
    engine._handle_websocket_message(event, data)
    engine.strategy.check_strategy.assert_called_once()

def test_execute_trade(engine):
    trade_signal = {'action': 'BUY', 'symbol': 'BTC-USDT', 'quantity': 0.01}
    engine.execute_trade(trade_signal)
    engine.api_client.create_order.assert_called_once_with(
        symbol='BTC-USDT',
        side='BUY',
        quantity=0.01,
        price=None,
        order_type='MARKET'
    )
