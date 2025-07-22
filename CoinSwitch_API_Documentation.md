# CoinSwitch API Documentation

## Change Log

**13th Dec 2024**

We have added a private user stream (socket) for balance updates. This can be used to get real-time balance updates of both the wallet and the portfolio whenever there is an update to any existing order.

**25th July 2024**

We have updated the Trading Fee API response to include discount and fee after discount.

**23rd July 2024**

**New Endpoints:**

*   Trading Fee `GET /trade/api/v2/tradingFee`

We have introduced an endpoint that will give you the fee applicable to you for an exchange.

**2nd July 2024**

*   To enhance security and better user experience, we have changed the way the signature is generated and added epoch time (in milliseconds) in the header. The same epoch time needs to be used for signature generation. To use any of the above APIs, you have to mandatorily move to the new security construct. The older construct will have different problems in terms of security and precision matching. Currently, the existing way of signature generation will work, but the same will be phased out by 15th of August.

**New Endpoints:**

*   Trade Info `GET /trade/api/v2/tradeInfo`

We have introduced an endpoint that will give you the basic details required to start your trading. This includes Exchange Precision, Min Max for the active coins on our platform.

*   TDS `GET /trade/api/v2/tds`

We have introduced an endpoint that will give you the TDS accumulated for your orders.
(Note: TDS from C2C orders will come with a delay of 1 day)

*   Server Time `GET /trade/api/v2/time`

**24th May 2024**

We have added a private user stream (socket) for order updates. This can be used to get real-time order updates on the orders that are placed during API trading across different exchanges.

**9th February 2024**

*   We have launched a new exchange c2c2 for USDT pairs.
*   We have changed the way the sockets are getting connected; the handshake path is changed from pro/realtime-rates-socket to pro/realtime-rates-socket/spot/{parameter}. This is backward compatible with the older version. The older version will be moved out by 1st of April 2024.

**16th January 2024**

*   The signature generation logic for Java is updated for better code execution by removing issues of precision, but the older one keeps working.

**26th December 2023**

*   Request limits for create order, portfolio, open order, and close order APIs have been updated.

**10th November 2023**

*   We have introduced WebSocket for candlestick data that fetches data in real-time at every 1-minute interval.
*   We have optimized closed order for receiving more data and thereby reducing the number of calls that need to be made. The default value of count in the request has been changed to 500, i.e., we can now get at max 500 latest data entries on a single call of closed order. We have removed total_orders_count in the response JSON of the closed order and open order API.

**6th November 2023**

In the Portfolio API, we have removed blocked_balance_deposit, blocked_balance_withdraw, blocked_balance_stake, and blocked_balance_vault response fields.

**25th September 2023**

We have introduced two new statuses: "CANCELLATION_RAISED" and "EXPIRATION_RAISED". It is an intermediate state.

CANCELLATION_RAISED means that we have asked the exchange to cancel the order, but it is not canceled on the exchange yet.

EXPIRATION_RAISED means that the order is getting expired from the broker end. During this period, order cancellation is not allowed.

**New Endpoints:**

*   Order Detail `GET /trade/api/v2/order`
*   Enabled Coins `GET /trade/api/v2/coins`
*   All responses will be consistent in terms of contract but will contain C2C pairs of USDT.
*   Parameters "S", "a", and "b" are removed from both Trade API and trade socket response.
*   "baseAsset" and "quoteAsset" are removed from both ticker API and ticker socket response.

**4th August 2023**

We have improved our V1 APIs:

*   Improved security in V2 APIs.
*   API responses have become consistent.

**New Endpoints:**

*   Validate Keys `GET /trade/api/v2/validate/keys`
*   Ping `GET /trade/api/v2/ping`
*   Create Order `POST /trade/api/v2/order`
*   Cancel Order `DELETE /trade/api/v2/order`
*   Open Order `GET /trade/api/v2/orders`
*   Close Order `GET /trade/api/v2/orders`
*   Portfolio `GET /trade/api/v2/user/portfolio`
*   Exchange Precision `POST /trade/api/v2/exchangePrecision`
*   24hr all pairs `GET /trade/api/v2/24hr/all-pairs/ticker`
*   24hr specific pair `GET /trade/api/v2/24hr/ticker`
*   Depth `GET /trade/api/v2/depth`
*   Trade `GET /trade/api/v2/trades`

## Streamline Your Trading Experience

Discover the power of CoinSwitch PRO API trading for spot and futures exchanges! This comprehensive guide will help you leverage our API to automate your trades, access real-time crypto rates, and create seamless integrations for your trading experience.

Our REST API is structured with user-friendly endpoints, giving you easy access to essential market data and exchange status information. We also provide private authenticated endpoints for advanced features such as trading and user-specific data. These endpoint requests need to be signed for enhanced security and protection for your transactions.

## Setting up an API Key

To fully utilize certain endpoints, you'll need an API key and a secret key. You can generate this key pair on your [CoinSwitch PRO Profile](https://coinswitch.co/pro/profile?section=api-trading).

In case you face any issues, please email your API key generation request to us at api@coinswitch.co. This step ensures an added layer of protection for your account and data.

**Remember:** Never share your API key or secret key with anyone. If your API keys have been unintentionally shared, we urge you to promptly delete them and generate a fresh key to maintain the highest level of security.

You can only have one API and one secret key active at a time.

## Information about our APIs

At CoinSwitch PRO, our base endpoint for API calls is https://coinswitch.co. All our endpoints for Spot and Futures provide responses in the form of JSON objects or arrays, ensuring easy integration with your applications.

To maintain consistency, all time and timestamp-related fields within our API follow a standardized format of milliseconds. This precision allows for accurate calculations and seamless data synchronization.

In each of the APIs, we need the following headers:

| Header | Value |
| --- | --- |
| Content-Type | application/json |
| X-AUTH-SIGNATURE | Signature that you need to generate at your end |
| X-AUTH-APIKEY | API key provided by Coinswitch |

## How to Setup

Begin API Trading on CoinSwitch PRO Spot and Futures by following the mentioned set-up steps based on your preferred client language.

### Python client

**Setup With PyCharm**

To set up a Python file in PyCharm, follow these step-by-step instructions:

**Install PyCharm**

Download and install the PyCharm community version IDE from the JetBrains website (https://www.jetbrains.com/edu-products/download/other-PCE.html). Choose the appropriate version for your operating system and install Python 3 as well.

**Create a new project**

Launch PyCharm and click on Create New Project on the welcome screen. If you already have a project open, you can also go to File -> New Project to create a new one.

**Configure project settings**

In the New Project dialog, choose the location where you want to store your project files and give your project a name. You can also specify the Python interpreter you want to use for this project. If you have a specific interpreter installed, select it; otherwise, you can choose the default option.

**Create a new Python file**

Once the project is created, you'll see the project structure on the left-hand side of the PyCharm window. Right-click on the directory where you want to create your Python file (e.g., the project root directory) and select New -> Python File. Give the file a meaningful name and press Enter.

**Write your Python code or paste the API trading Python file**

The newly created Python file will open in the editor window. You can start writing your Python code here or paste the API trading Python file that is shared with you over email. PyCharm provides features like syntax highlighting, code completion, and debugging assistance to help you during development.

**Install dependency**

Open PyCharm Terminal and run the below command:

```
pip install cryptography==40.0.2
pip install requests==2.27.1
pip install python-socketio==5.5.1
pip install websocket-client==1.2.3
```

**Run the Python file**

To run your Python file, you can right-click anywhere in the editor window and select Run from the context menu. Alternatively, you can use the keyboard shortcut (Ctrl+Shift+F10 on Windows/Linux or Shift+Control+R on macOS) to run the current Python file.

**View the output**

After running the Python file, you'll see the output in the Run tool window at the bottom of the PyCharm interface. If your program generates any output, it will be displayed here.

That's it! You have successfully set up the environment for API Trading.

**Note:** Please ensure you install Python 3.9 and the following libraries to their latest versions: cryptography, requests via your terminal in order to successfully run your scripts in your local machine without any virtual environment.

### Java Client

Here's a guide to help you get started with setting up a Java project with IntelliJ and Gradle:

**Install IntelliJ IDEA**

Download and install the latest version of IntelliJ IDEA from the official JetBrains website: https://www.jetbrains.com/idea/.

**Install Gradle**

Download and install Gradle by following the instructions on the official Gradle website: https://gradle.org/install/.

**Open Shared API Trading Gradle project in IntelliJ**

Launch IntelliJ IDEA and select Open Project on the welcome screen. Choose Gradle on the left panel and click Next. Select Java as the project type and click Next. Specify the project name and location, then click Finish.

**Configure Gradle in IntelliJ**

After creating the project, IntelliJ will prompt you to configure Gradle. Choose Use auto-import to automatically synchronize Gradle changes. Select the Gradle JVM (Java Virtual Machine) you want to use for your project.

**Configure project structure**

In the Project view on the left side of IntelliJ, navigate to the project folder. Right-click on the src folder, and you will see two files: the first one is the main Java file, and the second one is the config file. Specify the class name and click OK.

**Configure dependencies with Gradle**

Open the build.gradle file in the project root directory. Inside the dependencies block, specify the libraries and dependencies you want to include in your project. For example, to include the Apache Commons Lang library, you can add the following line:

```
dependencies {
    implementation 'org.apache.commons:commons-lang3:3.12.0'
}
```

**Build and run the project**

Click on the Gradle tab on the right side of the IntelliJ window. Expand the project tree and navigate to the Tasks section. Double-click on build to build the project. Once the build is successful, you can run the project by right-clicking on the Java class file and selecting Run.

Congratulations! You have set up the API Trading Java project with IntelliJ using Gradle as the build tool.

## Get Set Go

Add the received secret_key and api_key (keys shared over email or have been generated from Coinswitch Pro UI) in your script and start using API trading.

## Signature Generation

To access CoinSwitch APIs, you need to generate a signature and pass it as a header in each and every API call. In the request, sync the epoch time of your machine with the server time given by the following API.

### Server Time

```python
import json
import requests

payload={}

url = "https://coinswitch.co/trade/api/v2/time"

headers = {
  'Content-Type': 'application/json',
}


response = requests.request("GET", url, headers=headers, json=payload)
```

```java
public String getServerTime() throws Exception {
  HashMap<String, String> parameters = new HashMap<>();
  HashMap<String, Object> payload = new HashMap<>();

  return this.makeRequest("GET", "/trade/api/v2/time", payload, parameters);
}
```

> The above command returns JSON structured like this:

```json
{
    "serverTime": 1719905777483
}
```

Use the following endpoint to get server time. This server time will be used to validate the request epoch time passed in the header. It is recommended that the epoch time sent should be less than 5000ms, but if it's more than 60000ms, the request will fail.

### HTTP Request

**METHOD** `GET`
**ENDPOINT** `https://coinswitch.co/trade/api/v2/time`

```python
from cryptography.hazmat.primitives.asymmetric import ed25519
from urllib.parse import urlparse, urlencode
import urllib
import json
import time

# example method  ['GET', 'POST', 'DELETE']

# params represent the query params we need to pass during GET call

def get_signature(method, endpoint, params, epoch_time):
  unquote_endpoint = endpoint
  if method == "GET" and len(params) != 0:
      endpoint += ('&', '?')[urlparse(endpoint).query == ''] + urlencode(params)
      unquote_endpoint = urllib.parse.unquote_plus(endpoint)

  signature_msg = method + unquote_endpoint + epoch_time

  request_string = bytes(signature_msg, 'utf-8')
  secret_key_bytes = bytes.fromhex(secret_key)
  secret_key = ed25519.Ed25519PrivateKey.from_private_bytes(secret_key_bytes)
  signature_bytes = secret_key.sign(request_string)
  signature = signature_bytes.hex()
  return signature
```

```java
public class Main {
    public static void main(String[] args) throws Exception {
        Main main = new Main();
        HashMap<String, String> parameters = new HashMap<>();
        HashMap<String, Object> payload = new HashMap<>();

        String epochTime = System.currentTimeMillis()+"";
        String Response = main.generateSignature("GET", "/trade/api/v2/orders", parameters, epochTime);
        System.out.println(Response);
    }

  private String paramsToString(Map<String, String> params) throws Exception {
        StringBuilder sb = new StringBuilder();
        for (Map.Entry<String, String> entry : params.entrySet()) {
            if (sb.length() > 0) {
                sb.append("&");
            }
            sb.append(URLEncoder.encode(entry.getKey(), "UTF-8"));
            sb.append("=");
            sb.append(URLEncoder.encode(entry.getValue(), "UTF-8"));
        }
        return sb.toString();
    }

    private String signatureMessage(String method, String endpoint, String epochTime) throws Exception {
        return method + endpoint + epochTime;
    }

    public String getSignatureOfRequest(String secretKey, String requestString) {
        byte[] requestBytes = requestString.getBytes(StandardCharsets.UTF_8);
        byte[] secretKeyBytes = Hex.decode(secretKey);

        // Generate private key
        Ed25519PrivateKeyParameters privateKey = new Ed25519PrivateKeyParameters(secretKeyBytes, 0);

        // Sign the request
        Ed25519Signer signer = new Ed25519Signer();
        signer.init(true, privateKey);
        signer.update(requestBytes, 0, requestBytes.length);
        byte[] signatureBytes = signer.generateSignature();

        String signatureHex = Hex.toHexString(signatureBytes);
        return signatureHex;
    }

  public String generateSignature(String method, String endpoint, HashMap<String, String> params, String epochTime) throws Exception{
    String decodedEndpoint = endpoint;
    String secretKey = ""; // provided by coinswitch

    if (method.equals("GET") && !params.isEmpty()) {
        String query = new URI(endpoint).getQuery();
        endpoint += (query == null || query.isEmpty()) ? "?" : "&";
        endpoint += URLEncoder.encode(paramsToString(params), "UTF-8");
        decodedEndpoint = URLDecoder.decode(endpoint, "UTF-8");
    }

    String signatureMsg = signatureMessage(method, decodedEndpoint, epochTime);
    String signature = getSignatureOfRequest(secretKey, signatureMsg);
    return signature;
  }
}
```

> Let's take an example of a Get API:

```python
from cryptography.hazmat.primitives.asymmetric import ed25519
from urllib.parse import urlparse, urlencode
import urllib
import json
import requests
import time

params = {
    "count": 20,
    "from_time": 1600261657954,
    "to_time": 1687261657954,
    "side": "sell",
    "symbols": "btc/inr,eth/inr",
    "exchanges": "coinswitchx,wazirx",
    "type": "limit",
    "open": True
}

endpoint = "/trade/api/v2/orders"
method = "GET"
payload = {}

secret_key = <secret_key>  # provided by coinswitch
api_key = <api_key> # provided by coinswitch
epoch_time = str(int(time.time() * 1000))

unquote_endpoint = endpoint
if method == "GET" and len(params) != 0:
    endpoint += ('&', '?')[urlparse(endpoint).query == ''] + urlencode(params)
    unquote_endpoint = urllib.parse.unquote_plus(endpoint)

signature_msg = method + unquote_endpoint + epoch_time

request_string = bytes(signature_msg, 'utf-8')
secret_key_bytes = bytes.fromhex(secret_key)
secret_key = ed25519.Ed25519PrivateKey.from_private_bytes(secret_key_bytes)
signature_bytes = secret_key.sign(request_string)
signature = signature_bytes.hex()

url = "https://coinswitch.co" + endpoint

headers = {
  'Content-Type': 'application/json',
  'X-AUTH-SIGNATURE': signature,
  'X-AUTH-APIKEY': api_key,
  'X-AUTH-EPOCH': epoch_time
}

response = requests.request("GET", url, headers=headers, json=payload)
```

> Let's take an example of a DELETE API:

```python
from cryptography.hazmat.primitives.asymmetric import ed25519
from urllib.parse import urlparse, urlencode
import urllib
import json
import requests

payload = {
    "order_id": "698ed406-8ef5-4664-9779-f7978702a447"
}

endpoint = "/trade/api/v2/order"
method = "DELETE"
params = {}

secret_key = <secret_key>  # provided by coinswitch
api_key = <api_key> # provided by coinswitch

signature_msg = method + endpoint + json.dumps(payload, separators=(',', ':'), sort_keys=True)

request_string = bytes(signature_msg, 'utf-8')
secret_key_bytes = bytes.fromhex(secret_key)
secret_key = ed25519.Ed25519PrivateKey.from_private_bytes(secret_key_bytes)
signature_bytes = secret_key.sign(request_string)
signature = signature_bytes.hex()

url = "https://coinswitch.co" + endpoint

headers = {
  'Content-Type': 'application/json',
  'X-AUTH-SIGNATURE': signature,
  'X-AUTH-APIKEY': api_key
}

response = requests.request("DELETE", url, headers=headers, json=payload)
```

## Keys Validation

You can validate the keys provided by Coinswitch using the URL given below:

### HTTP Request

**METHOD** `GET`
**ENDPOINT** `https://coinswitch.co/trade/api/v2/validate/keys`

```json
RESPONSE 200
{
  "message":"Valid Access"
}

RESPONSE 401
{
  "message":"Invalid Access"
}
```

## Ping Testing

Use the code below to check if your ecosystem has been successfully connected to the CoinSwitch ecosystem.

```python
import requests
import json

url = "https://coinswitch.co/trade/api/v2/ping"
payload = {}

headers = {
  'Content-Type': 'application/json',
  'X-AUTH-SIGNATURE': <api-signature>,
  'X-AUTH-APIKEY': <api-key>
}

response = requests.request("GET", url, headers=headers, json=payload)
```

```java
public String ping() throws Exception {
    HashMap<String, String> parameters = new HashMap<>();
    HashMap<String, Object> payload = new HashMap<>();
    return this.makeRequest("GET", "/trade/api/v2/ping", payload, parameters);
}
```

```json
Response

{
  "message":"OK"
}
```

### HTTP Request

**METHOD** `GET`
**ENDPOINT** `https://coinswitch.co/trade/api/v2/ping`

## Introduction to C2C Trading

CoinSwitch PRO brings you the opportunity to trade your favorite cryptocurrencies using other cryptocurrencies. We have currently launched USDT Pairs for our traders to trade in. An active API trader would be able to place and successfully execute a crypto-to-crypto order on CoinSwitch PRO on these pairs. You can refer to the below illustration for better understanding.

Here is an example of a **BUY/SELL** C2C USDT Pair trade respectively for better trader understanding –

**[USDT - BTC]** — C2C Trade BUY
User can now use his/her available USDT from their balances and trade and acquire BTC on CoinSwitch PRO

**[BTC - USDT]** — C2C Trade SELL
User can sell away his/her existing cryptocurrency to obtain corresponding amount of USDT on CoinSwitch PRO

## SPOT Trading APIs

### Order Status Description

| Status | Description |
| --- | --- |
| OPEN | Order has not been executed at all |
| PARTIALLY_EXECUTED | Order has been partially executed |
| CANCELLED | User has cancelled the order |
| EXECUTED | Order has been executed |
| EXPIRED | Order has expired |
| DISCARDED | Order has not been processed (It has not been placed on the exchange) |
| CANCELLATION_RAISED | This is an intermediate state. We have requested the exchange to cancel the order. This status will come only when the order is cancelled on the exchange. |
| EXPIRATION_RAISED | This is an intermediate state. We have requested the exchange to expire the order. |

### Active Coins

Use the following endpoint to check all the active coins for an exchange:

**HTTP Request**

**METHOD** `GET`
**ENDPOINT** `https://coinswitch.co/trade/api/v2/coins`

**Request Parameters**

| Parameter | Type | Mandatory | Description |
| --- | --- | --- | --- |
| exchange | string | YES | Allowed values: “coinswitchx”/“wazirx”/“c2c1”/ “c2c2” (case insensitive) |

**Example**

```python
import requests
import json
from urllib.parse import urlparse, urlencode

params = {
    "exchange": "wazirx",
}
payload = {}

endpoint = "/trade/api/v2/coins"

endpoint += ('&', '?')[urlparse(endpoint).query == ''] + urlencode(params)

url = "https://coinswitch.co" + endpoint

headers = {
  'Content-Type': 'application/json',
  'X-AUTH-SIGNATURE': <api-signature>,
  'X-AUTH-APIKEY': <api-key>
}

response = requests.request("GET", url, headers=headers, json=payload)
```

> The above command returns JSON structured like this:

```json
Response: 200
{
    "data": {
        "wazirx": [
            "BAT/INR",
            "BNB/INR",
            "CHR/INR",
            "CRV/INR",
            "ETH/INR",
            "FTM/INR",
            "LRC/INR",
            "LTC/INR",
            "MKR/INR",
            "OGN/INR",
            "OMG/INR",
            "REQ/INR",
            "SXP/INR",
            "TRX/INR",
            "UMA/INR",
            "UNI/INR",
            "XLM/INR",
            "XRP/INR",
            "YFI/INR",
            "ZRX/INR",
            "BICO/INR",
            "COMP/INR",
            "COTI/INR",
            "DOGE/INR",
            "GALA/INR",
            "IOST/INR",
            "PEPE/INR",
            "SAND/INR",
            "USDT/INR",
            "YFII/INR",
            "1INCH/INR",
            "ALICE/INR",
            "JASMY/INR",
            "MATIC/INR"
        ]
    }
}
```

### Exchange Precision

Use the following endpoint to check precision coin and exchange wise:

**HTTP Request**

**METHOD** `POST`
**ENDPOINT** `https://coinswitch.co/trade/api/v2/exchangePrecision`

**Request Parameters**

| Parameter | Type | Mandatory | Description |
| --- | --- | --- | --- |
| exchange | string | Yes | (case insensitive) Allowed values: "coinswitchx"/ "wazirx" / "c2c1"/ "c2c2" |
| symbol | string | No | (case insensitive) Example: "BTC/INR" "SHIB/INR" "BTC/USDT" |

**Example**

```python
import requests
import json
from urllib.parse import urlparse, urlencode


url = "https://coinswitch.co/trade/api/v2/exchangePrecision"

payload = {
    "exchange": "coinswitchx",
    "symbol": "BTC/INR"
}

headers = {
  'Content-Type': 'application/json',
  'X-AUTH-SIGNATURE': <api-signature>,
  'X-AUTH-APIKEY': <api-key>
}

response = requests.request("POST", url, headers=headers, json=payload)
```

> The above command returns JSON structured like this:

```json
{
   "data":{
      "coinswitchx":{
         "BTC/INR":{
            "base":5,
            "quote":2,
            "limit":0
         }
      }
   }
}
```

### Trade Info

Use the following endpoint to check trading info:

**HTTP Request**

**METHOD** `GET`
**ENDPOINT** `https://coinswitch.co/trade/api/v2/tradeInfo`

**Request Parameters**

| Parameter | Type | Mandatory | Description |
| --- | --- | --- | --- |
| exchange | string | Yes | (case insensitive) Allowed values: "coinswitchx"/ "wazirx" / "c2c1"/ "c2c2" |
| symbol | string | No | (case insensitive) Example: "BTC/INR" "SHIB/INR" "BTC/USDT" |

**Example**

```python
import requests
import json

url = "https://coinswitch.co/trade/api/v2/tradeInfo"

params = {
  "exchange": "coinswitchx",
  "symbol": "BTC/INR"
}

headers = {
  'Content-Type': 'application/json',
  'X-AUTH-APIKEY': <api-key>
}

response = requests.request("GET", url, headers=headers, params=params)
```

> The above command returns JSON structured like this:

```json
{
  "data": {
    "coinswitchx": {
      "BTC/INR": {
        "quote": {
          "min": "150",
          "max": "2500000"
        },
        "precision": {
          "base": 6,
          "quote": 2,
          "limit": 0
        }
      }
    }
  }
}
```

### Trading Fee

**HTTP Request**

**METHOD** `GET`
**ENDPOINT** `https://coinswitch.co/trade/api/v2/tradingFee`

**Request Parameters**

| Parameter | Type | Mandatory | Description |
| --- | --- | --- | --- |
| exchange | string | Yes | (case insensitive) Allowed values: "coinswitchx"/ "wazirx" / "c2c1"/ "c2c2" |

**Example**

```python
import requests
import json

url = "https://coinswitch.co/trade/api/v2/tradingFee"

params = {
  "exchange": "coinswitchx",
}

headers = {
  'Content-Type': 'application/json',
  'X-AUTH-APIKEY': <api-key>,
  'X-AUTH-SIGNATURE': <signature>
}

response = requests.request("GET", url, headers=headers, params=params)
```

> The above command returns JSON structured like this:

```json
{
    "data": {
        "coinswitchx": {
            "AVAX": {
                "maker_fee": 0.0009,
                "taker_fee": 0.0009,
                "maker_discount_percentage": 100,
                "taker_discount_percentage": 100,
                "maker_fee_after_discount": 0,
                "taker_fee_after_discount": 0,
                "timestamp": 1721909805
            },
            "AXP": {
                "maker_fee": 0.0009,
                "taker_fee": 0.0009,
                "maker_discount_percentage": 100,
                "taker_discount_percentage": 100,
                "maker_fee_after_discount": 0,
                "taker_fee_after_discount": 0,
                "timestamp": 1721909805
            },
            "AXS": {
                "maker_fee": 0.0009,
                "taker_fee": 0.0009,
                "maker_discount_percentage": 100,
                "taker_discount_percentage": 100,
                "maker_fee_after_discount": 0,
                "taker_fee_after_discount": 0,
                "timestamp": 1721909805
            }
        }
    }
}
```
