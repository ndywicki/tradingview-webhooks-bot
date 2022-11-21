# Tradingview Webhook bot

This webhook bot handle HTTP requests sent by [TradingView](https://tradingview.com/) alerts that are base on yours indicators or strategies.
The default market exhange broker is [ByBit](https://www.bybit.com/en-US/invite?ref=YMPJKN%230) and especially for PERPetual crypto futures market.

You can create ByBit account with my referral code `YMPJKN#0` to gain ZERO-fee Spot trading and earn up to 250 USDT.

# Prerequisis

Install Python3 and Virtualenv (https://news.julien-anne.fr/ubuntu-20-04-python3-et-virtualenv-installation-et-erreurs-potentielles/)
Then install requirements:

```
pip3 install -r requirements.txt
```

# Configuration

To use your own BYBIT API credentials create an `.env` file in the root project directory with the content:

```bash
PIN=Set this to something unique
API_KEY=YOUR_API_KEY
API_SECRET=YOUR_API_SECRET
PERCENT_BALANCE=90 # Percentage of your wallet balance used (without leverage) to open order
```

## API key

A basic API key check is purpose to secure at least.
Once your PIN secret code is set you can display the generate value:
```
(virtualenv)> python3 auth.py 
```

The `key` value should be set in the HTTP json payload (see below)

# Running

Simple use the python command or use the systemD service (see below)

```
(virtualenv)> python3 webhook-bot.py 
```

By default the bot listen on the port `5000`, of course it should be exposed outside your network.
You can use https://ngrok.com/ service to expose easily your local app bot.

# Strategies

The bot come from with a simple strategy that close all positions and create new one on the PERP* markets.
Look under `strategies` directory.
You can create your own strategy and add the process call in `webhook-bot.py`:

```python
if get_token() == data['key']:
    print('POST Received:', data)
    SimpleStrategy.process(exchange, data)
    YourOwnStrategy.process(exchange, data)
    return '', 200
```

# Tradingview Alert message format

You can use this alert message sample to create a basic alert for the `SimpleStrategy`

```json
{
	"strategy": "simple-strategy",
	"type": "market",
	"side": "{{strategy.order.action}}",
	"symbol": "{{ticker}}",
	"price": "{{strategy.order.price}}",
	"key": "yourkey"
}
```

With:

* `strategy`: The name of strategy to use if you have many strategies
* `key`: The API key that match the encoded pin in `auth.py`
* Other params come from the TradingView alert placeholders see https://www.tradingview.com/support/solutions/43000531021-how-to-use-a-variable-value-in-alert/

# Option install as Ubuntu SystemD service

You can create a SystemD service, see under the `scripts` directory.
