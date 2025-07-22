Here is the Product Requirements Document (PRD) for the new crypto futures trading bot.

-----

# **Product Requirements Document: Python Crypto Futures Trading Bot**

**Document Version:** 1.0
**Date:** July 23, 2025
**Author:** Gemini (Expert Product Manager)
**Status:** Draft

-----

## 1\. Introduction

This document outlines the requirements for a new Python-based crypto futures trading bot. The primary goal is to provide a secure, reliable, and easy-to-use tool for semi-technical users to automate their trading strategies on the CoinSwitch Pro platform.

### Problem

The cryptocurrency market is highly volatile and operates 24/7, making it impossible for traders to monitor price movements and execute trades manually at all times. Manual trading is also susceptible to emotional decision-making and execution delays, which can lead to missed opportunities and losses. Traders need an automated solution that can execute their predefined strategies tirelessly and precisely.

### Vision

To empower retail cryptocurrency traders with a simple, secure, and customizable open-source tool that automates futures trading on CoinSwitch Pro, enabling them to execute complex strategies programmatically without needing to build the underlying trading infrastructure from scratch.

### Goals/Objectives (MVP)

  * **Functionality:** Successfully execute `long` and `short` futures trades on CoinSwitch Pro based on a user-defined strategy file.
  * **Reliability:** Achieve and maintain an uptime of \>= 99.5% during active trading sessions.
  * **Performance:** Process user commands from the Telegram interface with a response latency of \< 2 seconds.
  * **Security:** Ensure no sensitive credentials (API keys, tokens) are hardcoded in the application source code.
  * **Usability:** Provide a clear and comprehensive setup guide that allows a target user to configure and run the bot in under 15 minutes.

-----

## 2\. User Personas

### "The Hobbyist Coder" (Primary Persona)

  * **Description:** A tech-savvy individual, possibly in a software or IT role, who trades crypto as a serious hobby. They are comfortable with Python scripting but are not necessarily experts in building robust, production-grade applications.
  * **Goals:**
      * To test and automate their trading ideas without building an entire bot from the ground up.
      * Wants a simple framework where they can just "plug in" their strategy logic.
      * Needs a way to monitor and control their bot remotely.
  * **Technical Skills:** Intermediate Python, comfortable with the command line and editing configuration files.

### "The Experienced Trader" (Secondary Persona)

  * **Description:** A trader with significant market experience but limited programming skills. They understand technical indicators and complex trading strategies deeply.
  * **Goals:**
      * To remove emotion and manual execution errors from their trading.
      * To find an "out-of-the-box" solution that they can run with minimal setup, possibly with help from a more technical friend to script the strategy.
  * **Technical Skills:** Basic computer literacy. Can follow a detailed setup guide but is not a coder.

-----

## 3\. Features & Requirements

### 3.1. Core Trading Engine

The engine is the heart of the bot, responsible for connecting to the exchange, fetching data, and executing trades.

  * **FR-1.1:** The entire application MUST be built using **Python** (version 3.9 or higher).
  * **FR-1.2:** It MUST integrate with the **CoinSwitch Pro API**.
      * Use the REST API for state-changing actions: creating orders, cancelling orders, and fetching account balance/positions.
      * Use WebSockets for receiving real-time market data (e.g., price ticks) to minimize latency and trigger strategy evaluation.
  * **FR-1.3:** The bot MUST feature a **Pluggable Strategy Module**.
      * The core application logic will be separate from the user's trading strategy.
      * Users will define their trading logic in a dedicated file named `strategy.py`.
      * The main bot application will dynamically import and execute a function from `strategy.py` on each market data update.
      * A well-commented example `strategy.py.example` file MUST be provided, demonstrating a simple strategy (e.g., a moving average crossover) to guide the user.

<!-- end list -->

```python
# strategy.py.example - A simple example of a user-defined strategy file.
# The user would copy this to strategy.py and customize it.

def check_strategy(dataframe):
    """
    Analyzes market data and decides whether to enter a trade.
    
    Args:
        dataframe (pandas.DataFrame): A DataFrame containing the latest market data (e.g., OHLCV).
        
    Returns:
        dict or None: A dictionary defining the trade action or None to do nothing.
        Example: {'action': 'BUY', 'symbol': 'BTC-USDT', 'quantity': 0.01}
    """
    # Example: Simple Moving Average Crossover Strategy
    df = dataframe.copy()
    df['sma_short'] = df['close'].rolling(window=10).mean()
    df['sma_long'] = df['close'].rolling(window=50).mean()
    
    last_row = df.iloc[-1]
    
    # Buy signal
    if last_row['sma_short'] > last_row['sma_long']:
        return {'action': 'BUY', 'symbol': 'BTC-USDT', 'quantity': 0.01}
        
    # Sell signal
    elif last_row['sma_short'] < last_row['sma_long']:
        return {'action': 'SELL', 'symbol': 'BTC-USDT', 'quantity': 0.01}
        
    return None
```

### 3.2. Telegram Bot Interface

A simple, secure interface for remote monitoring and control.

  * **FR-2.1:** The bot MUST be controllable via a Telegram Bot interface.
  * **FR-2.2:** The following commands MUST be supported:
      * `/start`: Responds with a confirmation message that the bot is running (e.g., "✅ Trading bot is active.").
      * `/balance`: Fetches and displays the user's current futures account balance from CoinSwitch Pro.
      * `/positions`: Fetches and displays a list of all currently open futures positions, including symbol, quantity, entry price, and direction (long/short).
      * `/stop`: Initiates a graceful shutdown. It must cancel all open orders on the exchange before terminating the trading process.

### 3.3. Security & Configuration

Security is paramount. User credentials must be handled safely.

  * **FR-3.1:** All sensitive credentials, including `COINSWITCH_API_KEY`, `COINSWITCH_API_SECRET`, and `TELEGRAM_BOT_TOKEN`, MUST be loaded from a `.env` file at runtime.
  * **FR-3.2:** The application MUST NOT contain any hardcoded credentials.
  * **FR-3.3:** A `.env.example` file MUST be included in the project repository to serve as a template for users.
  * **FR-3.4:** The `.gitignore` file MUST be pre-configured to ignore `.env` files to prevent accidental commits of user secrets.

### 3.4. Reliability & Logging

The bot must be resilient and provide clear logs for debugging and record-keeping.

  * **FR-4.1:** Implement robust error handling for common failures, such as API connection timeouts or invalid responses from the exchange. The bot should attempt to reconnect using an exponential backoff strategy.
  * **FR-4.2:** Critical errors that prevent trading (e.g., invalid API keys, repeated connection failures) MUST trigger a notification to the user via the Telegram bot.
  * **FR-4.3:** All significant events MUST be logged to a local file named `trading_bot.log`.
  * **FR-4.4:** Logged events must include: bot startup/shutdown, trade execution attempts, successful trade confirmations, and all errors. Each log entry must be timestamped.

-----

## 4\. Technical & Documentation Requirements

  * **TR-1:** A **Beginner-Friendly README.md** file is required. It must contain clear, step-by-step instructions for:
      * Installation of dependencies (`requirements.txt`).
      * Configuration (creating the `.env` file, obtaining API keys).
      * Customizing the `strategy.py` file.
      * Running the bot.
  * **TR-2:** A brief **Architecture Document** (`ARCHITECTURE.md`) must be created. It should include a simple diagram and text explaining how the main components (Core Engine, Strategy Module, Telegram Bot, CoinSwitch Pro API) interact.
  * **TR-3:** The project MUST include a testing suite using the **`pytest`** framework. It should contain sample unit tests to demonstrate the testing setup and encourage contributions.

-----

## 5\. Success Metrics

The success of the MVP will be measured by the following key metrics:

  * **Reliability - Bot Uptime:** \> 99.5% uptime during a 7-day continuous run test.
  * **Performance - Trade Execution Latency:** The time between a strategy generating a signal and the order being successfully acknowledged by the CoinSwitch Pro API should be \< 500ms.
  * **Stability - Error Rate:** \< 1% of initiated trades fail due to unhandled exceptions within the bot's code.
  * **Adoption - User Feedback:** Positive qualitative feedback from at least 10 beta testers confirming they can successfully set up and run the bot.

-----

## 6\. Out of Scope (Future Work)

The following features will **not** be included in this initial version but may be considered for future releases:

  * A web-based or graphical user interface (GUI).
  * Support for multiple cryptocurrency exchanges.
  * An integrated backtesting engine to test strategies against historical data.
  * Advanced performance analytics dashboards.
  * Support for spot market trading.
  * Persistence of trade history to a database.