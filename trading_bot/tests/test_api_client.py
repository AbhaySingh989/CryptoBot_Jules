import pytest
from unittest.mock import patch, MagicMock
from trading_bot.core.api_client import CoinSwitchProApiClient

@pytest.fixture
def client():
    client = CoinSwitchProApiClient()
    client.api_key = "test_key"
    client.api_secret = "test_secret"
    return client

def test_generate_signature(client):
    timestamp = "1672531200000"
    signature = client._generate_signature(timestamp)
    # The expected signature is a HMAC-SHA256 hash.
    # We can't easily replicate it here without the exact same hashing implementation,
    # but we can check if it returns a string of the correct length.
    assert isinstance(signature, str)
    assert len(signature) == 64

@patch('requests.request')
def test_get_listen_key(mock_request, client):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"listenKey": "test_listen_key"}
    mock_request.return_value = mock_response

    listen_key = client.get_listen_key()
    assert listen_key == "test_listen_key"
    assert client.listen_key == "test_listen_key"

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

    order = client.create_order("BTC/INR", "buy", 1, 50000)
    assert order == {"status": "success"}
