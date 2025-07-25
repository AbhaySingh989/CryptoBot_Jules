import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from trading_bot.core.config import TELEGRAM_BOT_TOKEN
from trading_bot.core.trading_engine import TradingEngine

class TelegramBot:
    def __init__(self, trading_engine: TradingEngine):
        self.trading_engine = trading_engine
        self.application = None

    def setup(self):
        """Sets up the Telegram bot application."""
        self.application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(CommandHandler("balance", self.balance))
        self.application.add_handler(CommandHandler("positions", self.positions))
        self.application.add_handler(CommandHandler("stop", self.stop))

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Sends a confirmation message when the /start command is issued."""
        await update.message.reply_text("✅ Trading bot is active.")

    async def balance(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Fetches and displays the user's current futures account balance."""
        balance_info = self.trading_engine.api_client.get_balance()
        if balance_info:
            await update.message.reply_text(f"Balance: {balance_info}")
        else:
            await update.message.reply_text("Could not fetch balance.")

    async def positions(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Fetches and displays a list of all currently open futures positions."""
        positions_info = self.trading_engine.api_client.get_positions()
        if positions_info:
            await update.message.reply_text(f"Positions: {positions_info}")
        else:
            await update.message.reply_text("Could not fetch positions.")

    async def stop(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Initiates a graceful shutdown of the bot."""
        self.trading_engine.stop()
        await update.message.reply_text("Trading bot is shutting down...")

    def run(self):
        """Starts the Telegram bot."""
        self.setup()
        self.application.run_polling()
