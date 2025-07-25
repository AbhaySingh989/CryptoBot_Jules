import asyncio
import argparse
from trading_bot.core.trading_engine import TradingEngine
from trading_bot.core.logging_config import setup_logging

async def main():
    parser = argparse.ArgumentParser(description='Crypto Trading Bot')
    parser.add_argument('--api-key', type=str, help='CoinSwitch Pro API Key')
    parser.add_argument('--api-secret', type=str, help='CoinSwitch Pro API Secret')
    parser.add_argument('--no-websocket', action='store_true', help='Disable WebSocket connection')
    args = parser.parse_args()

    setup_logging()
    engine = TradingEngine()
    # Set the API key and secret if they are provided as arguments
    if args.api_key:
        engine.api_client.api_key = args.api_key
    if args.api_secret:
        engine.api_client.api_secret = args.api_secret

    await engine.start(no_websocket=args.no_websocket)


if __name__ == "__main__":
    asyncio.run(main())
