import pytest
from unittest.mock import MagicMock, patch
from trading_bot.core.trading_engine import TradingEngine

@pytest.fixture
def engine():
    with patch('importlib.import_module') as mock_import:
        mock_strategy = MagicMock()
        mock_import.return_value = mock_strategy
        engine = TradingEngine()
        engine.strategy = mock_strategy
        return engine

def test_load_strategy(engine):
    assert engine.strategy is not None

@pytest.mark.asyncio
async def test_handle_websocket_message(engine):
    message = {"data": "test_message"}
    await engine._handle_websocket_message(message)
    engine.strategy.check_strategy.assert_called_once_with(message)

def test_execute_trade(engine):
    trade_signal = {'action': 'BUY', 'symbol': 'BTC-USDT', 'quantity': 0.01}
    with patch.object(engine, 'api_client', new_callable=MagicMock) as mock_api_client:
        engine.execute_trade(trade_signal)
        # We'll expand this test later to check the actual API call
        assert mock_api_client.create_order.called == False # Not implemented yet
