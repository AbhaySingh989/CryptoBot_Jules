# Python Crypto Futures Trading Bot

This is a Python-based crypto futures trading bot that uses the CoinSwitch Pro API to automate trading strategies.

## Features

-   Connects to the CoinSwitch Pro API for real-time market data and trade execution.
-   Pluggable strategy module for easy customization of trading logic.
-   Console interface for monitoring and controlling the bot.
-   Securely loads API keys and other credentials from a `.env` file.
-   Logs all important events to a local file (`trading_bot.log`).

## Installation

1.  Clone the repository:
    ```
    git clone https://github.com/your-username/crypto-trading-bot.git
    ```
2.  Install the dependencies:
    ```
    pip install -r requirements.txt
    ```

## Configuration

1.  Create a `.env` file in the root directory of the project by copying the `.env.example` file:
    ```
    cp .env.example .env
    ```
2.  Open the `.env` file and add your CoinSwitch Pro API key and secret, and your Telegram bot token.

## Usage

1.  Customize your trading strategy by editing the `strategy.py` file in the `trading_bot/strategies` directory. You can use the `strategy.py.example` file as a template.
2.  Run the bot:
    ```
    python -m trading_bot
    ```

## Architecture

For a detailed explanation of the bot's architecture, please see the `ARCHITECTURE.md` file.
