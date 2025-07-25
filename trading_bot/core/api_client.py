import datetime
import time
import concurrent.futures
from cryptography.hazmat.primitives.asymmetric import ed25519
import json
import requests
import socketio
import asyncio
from trading_bot.core.config import COINSWITCH_API_KEY, COINSWITCH_API_SECRET

class CoinSwitchProApiClient:
    def __init__(self):
        self.api_key = COINSWITCH_API_KEY
        self.api_secret = COINSWITCH_API_SECRET
        self.base_url = "https://coinswitch.co"
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json"
        })

    def _generate_signature(self, method, endpoint, payload, epoch_time):
        message = method + endpoint + epoch_time
        request_string = bytes(message, 'utf-8')
        secret_key_bytes = bytes.fromhex(self.api_secret)
        secret_key = ed25519.Ed25519PrivateKey.from_private_bytes(secret_key_bytes)
        signature_bytes = secret_key.sign(request_string)
        return signature_bytes.hex()

    def _make_request(self, method, endpoint, params=None, data=None):
        decoded_endpoint = endpoint
        if method == "GET" and params:
            endpoint += '?' + '&'.join([f"{key}={value}" for key, value in params.items()])
            decoded_string = endpoint.replace('+', ' ')
            decoded_endpoint = requests.utils.unquote(decoded_string)

        epoch_time = str(int(datetime.datetime.now().timestamp() * 1000))

        signature = self._generate_signature(method, decoded_endpoint, data, epoch_time)

        headers = {
            "X-AUTH-SIGNATURE": signature,
            "X-AUTH-APIKEY": self.api_key,
            "X-AUTH-EPOCH": epoch_time,
            "X-REQUEST-ID": "trading_bot" + epoch_time,
            "Content-Type": "application/json"
        }

        url = f"{self.base_url}{endpoint}"

        try:
            response = self.session.request(method, url, headers=headers, json=data, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error making request to {endpoint}: {e}")
            return None

    def get_listen_key(self):
        """Fetches a new listenKey from the REST API."""
        endpoint = "/trade/api/v2/user/listenKey"
        return self._make_request("POST", endpoint)

    async def get_balance(self):
        """Fetches the user's futures account balance."""
        endpoint = "/trade/api/v2/futures/wallet_balance"
        try:
            return await asyncio.wait_for(asyncio.to_thread(self._make_request, "GET", endpoint), timeout=10)
        except asyncio.TimeoutError:
            print("get_balance timed out")
            return None

    async def get_positions(self):
        """Fetches the user's open futures positions."""
        endpoint = "/trade/api/v2/futures/positions"
        try:
            return await asyncio.wait_for(asyncio.to_thread(self._make_request, "GET", endpoint), timeout=10)
        except asyncio.TimeoutError:
            print("get_positions timed out")
            return None

    def create_order(self, symbol, side, quantity, price, order_type="LIMIT", reduce_only=False, trigger_price=None):
        """Creates a new order."""
        endpoint = "/trade/api/v2/futures/order"
        data = {
            "exchange": "EXCHANGE_2",
            "symbol": symbol,
            "side": side,
            "quantity": quantity,
            "order_type": order_type,
            "reduce_only": reduce_only
        }
        if price:
            data["price"] = price
        if trigger_price:
            data["trigger_price"] = trigger_price

        return self._make_request("POST", endpoint, data=data)

    def cancel_order(self, order_id):
        """Cancels an existing order."""
        endpoint = "/trade/api/v2/futures/order"
        data = {
            "exchange": "EXCHANGE_2",
            "order_id": order_id
        }
        return self._make_request("DELETE", endpoint, data=data)

    def get_depth(self, symbol):
        endpoint = "/trade/api/v2/futures/order_book"
        params = {"symbol": symbol, "exchange": "EXCHANGE_2"}
        return self._make_request("GET", endpoint, params=params)

    def get_trades(self, symbol):
        endpoint = "/trade/api/v2/futures/trades"
        params = {"symbol": symbol, "exchange": "EXCHANGE_2"}
        return self._make_request("GET", endpoint, params=params)

    def get_candlestick_data(self, symbol, interval, limit=100):
        endpoint = "/trade/api/v2/futures/klines"
        params = {"symbol": symbol, "interval": interval, "limit": limit, "exchange": "EXCHANGE_2"}
        return self._make_request("GET", endpoint, params=params)

    async def start_websocket(self, message_handler, test_mode=False):
        sio = socketio.AsyncClient(logger=True, engineio_logger=True)

        @sio.event
        async def connect():
            print("Connected to WebSocket")
            # Subscribe to the BTCUSDT candlestick data
            await sio.emit("FETCH_CANDLESTICK_CS_PRO", {"event": "subscribe", "pair": "BTCUSDT_1"}, namespace="/exchange_2")

        @sio.event
        async def disconnect():
            print("Disconnected from WebSocket")

        @sio.on("*", namespace="/exchange_2")
        async def catch_all(event, data):
            message_handler(event, data)
            if test_mode and event == "FETCH_CANDLESTICK_CS_PRO":
                await sio.disconnect()

        try:
            await sio.connect(
                "wss://ws.coinswitch.co",
                namespaces=["/exchange_2"],
                transports=["websocket"],
                socketio_path="/pro/realtime-rates-socket/futures/exchange_2"
            )
        except Exception as e:
            print(f"WebSocket connection failed: {e}")
