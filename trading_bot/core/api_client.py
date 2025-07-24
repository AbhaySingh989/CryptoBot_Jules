import hashlib
import hmac
import asyncio
import json
import time
import requests
import websockets
from trading_bot.core.config import COINSWITCH_API_KEY, COINSWITCH_API_SECRET

class CoinSwitchProApiClient:
    def __init__(self):
        self.api_key = COINSWITCH_API_KEY
        self.api_secret = COINSWITCH_API_SECRET
        self.base_rest_url = "https://coinswitch.co"
        self.base_ws_url = "wss://api-trading.coinswitch.co"
        self.listen_key = None

    def _generate_signature(self, timestamp, payload_str=""):
        """Generates the HMAC-SHA256 signature for a signed REST request."""
        message = f"{timestamp}{self.api_key}{payload_str}"
        signature = hmac.new(
            self.api_secret.encode('utf-8'),
            message.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        return signature

    def _make_request(self, method, endpoint, params=None, data=None):
        url = self.base_rest_url + endpoint
        timestamp = str(int(time.time() * 1000))

        headers = {
            'x-api-key': self.api_key,
            'x-api-timestamp': timestamp,
            'Content-Type': 'application/json'
        }

        payload_str = json.dumps(data, separators=(',', ':')) if data else ""
        headers['x-api-signature'] = self._generate_signature(timestamp, payload_str)

        try:
            response = requests.request(method, url, headers=headers, params=params, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error making request to {endpoint}: {e}")
            return None

    def get_listen_key(self):
        """Fetches a new listenKey from the REST API."""
        endpoint = "/trade/api/v2/user/listenKey"
        response = self._make_request("POST", endpoint)
        if response and 'listenKey' in response:
            self.listen_key = response['listenKey']
            print(f"Successfully obtained listenKey: {self.listen_key[:10]}...")
            return self.listen_key
        return None

    def get_balance(self):
        """Fetches the user's futures account balance."""
        endpoint = "/trade/api/v2/user/portfolio"
        return self._make_request("GET", endpoint)

    def get_positions(self):
        """Fetches the user's open futures positions."""
        # The documentation does not specify a dedicated endpoint for futures positions.
        # We will assume for now that the portfolio endpoint contains this information.
        # This might need to be adjusted based on actual API responses.
        return self.get_balance()

    def create_order(self, symbol, side, quantity, price, order_type="LIMIT"):
        """Creates a new order."""
        endpoint = "/trade/api/v2/order"
        data = {
            "symbol": symbol,
            "side": side,
            "quantity": quantity,
            "price": price,
            "type": order_type
        }
        return self._make_request("POST", endpoint, data=data)

    def cancel_order(self, order_id):
        """Cancels an existing order."""
        endpoint = "/trade/api/v2/order"
        data = {"order_id": order_id}
        return self._make_request("DELETE", endpoint, data=data)

    async def start_private_stream(self, message_handler):
        """Connects to the private user data stream and handles messages."""
        if not self.get_listen_key():
            return

        ws_url = f"{self.base_ws_url}/ws/{self.listen_key}"

        while True:
            try:
                async with websockets.connect(ws_url) as websocket:
                    print("Connected to private WebSocket stream.")
                    while True:
                        message = await websocket.recv()
                        data = json.loads(message)
                        await message_handler(data)

            except websockets.exceptions.ConnectionClosed as e:
                print(f"Private WebSocket connection closed: {e}. Reconnecting...")
                # Implement exponential backoff here before retrying
                await asyncio.sleep(5)
                # Fetch a new listen key upon reconnection
                if not self.get_listen_key():
                    await asyncio.sleep(10) # Wait longer if auth fails
                    continue
                ws_url = f"{self.base_ws_url}/ws/{self.listen_key}"

            except Exception as e:
                print(f"An error occurred: {e}")
                await asyncio.sleep(10)
