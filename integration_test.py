import asyncio
import os
import sys

async def main():
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()

    from trading_bot.core.trading_engine import TradingEngine

    engine = TradingEngine()
    engine.api_client.api_key = os.getenv("COINSWITCH_API_KEY")
    engine.api_client.api_secret = os.getenv("COINSWITCH_API_SECRET")

    # Test the REST API functionality
    balance = engine.api_client.get_balance()
    print(f"Balance: {balance}")
    assert balance is not None

    positions = engine.api_client.get_positions()
    print(f"Positions: {positions}")
    assert positions is not None


if __name__ == "__main__":
    # Add the project root to the Python path
    sys.path.insert(0, '.')
    asyncio.run(main())
