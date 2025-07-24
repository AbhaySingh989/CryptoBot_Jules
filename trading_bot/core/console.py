import asyncio
from trading_bot.core.trading_engine import TradingEngine

class ConsoleInterface:
    def __init__(self, trading_engine: TradingEngine):
        self.trading_engine = trading_engine

    async def start(self):
        while True:
            command = await asyncio.to_thread(input, "Enter command: ")
            if command == "balance":
                balance = self.trading_engine.api_client.get_balance()
                print(f"Balance: {balance}")
            elif command == "positions":
                positions = self.trading_engine.api_client.get_positions()
                print(f"Positions: {positions}")
            elif command == "stop":
                self.trading_engine.stop()
                break
            else:
                print("Unknown command")
