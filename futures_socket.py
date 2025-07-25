import socketio

# Initialize Socket.IO client with logging enabled
sio = socketio.Client(logger=True, engineio_logger=True)

# Configuration
BASE_URL = "wss://ws.coinswitch.co"
NAMESPACE = "/exchange_2"  # Correct namespace
SOCKET_PATH = "/pro/realtime-rates-socket/futures/exchange_2"  # Correct handshake path

# Event Names
EVENT_ORDER_BOOK = "FETCH_ORDER_BOOK_CS_PRO"
EVENT_TICKER_INFO = "FETCH_TICKER_INFO_CS_PRO"
EVENT_TRADES = "FETCH_TRADES_CS_PRO"
EVENT_CANDLES = "FETCH_CANDLESTICK_CS_PRO"

# Trading pair
PAIR = "BTCUSDT"

## FOR CANDLES use PAIR like coinnames separated by "_" and minute
#PAIR = "BTCUSDT_5"


def connect_to_socket():
    """Establishes a WebSocket connection."""
    try:
        sio.connect(
            BASE_URL,
            namespaces=[NAMESPACE],
            transports=["websocket"],
            socketio_path=SOCKET_PATH,
            wait=True,
            wait_timeout=10
            #headers={"Authorization": ""}  # Ensure this is required, otherwise remove it
        )
        print("✅ Connected successfully!")
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        exit()


def subscribe_to_event(event_name):
    """Subscribes to a specific event with the given trading pair."""
    subscribe_data = {"event": "subscribe", "pair": PAIR}
    sio.emit(event_name, subscribe_data, namespace=NAMESPACE)
    print(f"📩 Subscribed to {PAIR} for event: {event_name}")


# Event handler for Order Book updates
@sio.on(EVENT_ORDER_BOOK, namespace=NAMESPACE)
def handle_order_book(data):
    print("📊 Order Book Update:", data)


# Event handler for Ticker Info updates
@sio.on(EVENT_TICKER_INFO, namespace=NAMESPACE)
def handle_ticker_info(data):
    print("📈 Ticker Info Update:", data)


# Event handler for Trade Execution updates
@sio.on(EVENT_TRADES, namespace=NAMESPACE)
def handle_trades(data):
    print("💹 Trade Execution Update:", data)

@sio.on(EVENT_CANDLES, namespace=NAMESPACE)
def handle_candles(data):
    print("🕯️ Candlestick Update:", data)


if __name__ == "__main__":
    # Connect to WebSocket
    connect_to_socket()

    # Subscribe to events
    #subscribe_to_event(EVENT_ORDER_BOOK)
    #subscribe_to_event(EVENT_TICKER_INFO)
    subscribe_to_event(EVENT_TRADES)
    #subscribe_to_event(EVENT_CANDLES)

    # Keep connection alive
    sio.wait()
