import asyncio
import importlib
import logging
import pandas as pd
from trading_bot.core.api_client import CoinSwitchProApiClient

class TradingEngine:
    def __init__(self):
        self.api_client = CoinSwitchProApiClient()
        self.strategy = self._load_strategy()
        self.ohlcv = {}

    def _load_strategy(self):
        try:
            return importlib.import_module("trading_bot.strategies.strategy")
        except ImportError:
            logging.error("Strategy file not found. Please create a strategy.py file in the strategies directory.")
            return None

    def _handle_websocket_message(self, event, data):
        if event == 'FETCH_CANDLESTICK_CS_PRO':
            self._update_ohlcv(data)
            if self.strategy:
                df = pd.DataFrame(self.ohlcv[data['s']])
                trade_signal = self.strategy.check_strategy(df)
                if trade_signal:
                    self.execute_trade(trade_signal)

    def _update_ohlcv(self, data):
        symbol = data['s']
        if symbol not in self.ohlcv:
            self.ohlcv[symbol] = []

        # This is a simplified approach. A more robust solution would be to manage a
        # proper OHLCV dataframe and update it with each new candle.
        self.ohlcv[symbol].append({
            'open': data['o'],
            'high': data['h'],
            'low': data['l'],
            'close': data['c'],
            'volume': data['v'],
            'timestamp': data['t']
        })

    def execute_trade(self, trade_signal):
        logging.info(f"Executing trade: {trade_signal}")
        self.api_client.create_order(
            symbol=trade_signal['symbol'],
            side=trade_signal['action'],
            quantity=trade_signal['quantity'],
            price=None, # For market orders
            order_type="MARKET"
        )

    async def start(self, no_websocket=False):
        if not self.strategy:
            return

        logging.info("Starting trading engine...")
        # Start the websocket
        if not no_websocket:
            await self.api_client.start_websocket(self._handle_websocket_message)

    def stop(self):
        logging.info("Stopping trading engine...")
        # The socketio client doesn't have a simple stop method.
        # In a real application, we would need to manage the socket connection
        # more carefully to allow for a graceful shutdown.
        pass
