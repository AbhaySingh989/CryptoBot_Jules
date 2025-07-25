import pytest
from unittest.mock import patch, MagicMock
from trading_bot.core.api_client import CoinSwitchProApiClient

@pytest.fixture
def client():
    client = CoinSwitchProApiClient()
    client.api_key = "test_key"
    client.api_secret = "0000000000000000000000000000000000000000000000000000000000000000" # 64 hex characters
    return client

def test_generate_signature(client):
    method = "POST"
    endpoint = "/trade/api/v2/futures/order"
    payload = {"symbol": "BTCUSDT", "side": "BUY", "quantity": 1, "order_type": "MARKET"}
    epoch_time = "1672531200000"
    signature = client._generate_signature(method, endpoint, payload, epoch_time)
    assert isinstance(signature, str)
    assert len(signature) == 128

@patch('requests.request')
def test_get_balance(mock_request, client):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"balance": 1000}
    mock_request.return_value = mock_response

    balance = client.get_balance()
    assert balance == {"balance": 1000}

@patch('requests.request')
def test_create_order(mock_request, client):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"status": "success"}
    mock_request.return_value = mock_response

    order = client.create_order("BTCUSDT", "BUY", 1, 50000, order_type="LIMIT")
    assert order == {"status": "success"}
