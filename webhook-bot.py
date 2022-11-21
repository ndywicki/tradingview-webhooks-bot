"""
Tradingview-webhooks-bot is a python bot that works with tradingview's webhook alerts!
This bot is not affiliated with tradingview and was created by @robswc

You can follow development on github at: github.com/ndywicki/tradingview-webhooks-bot

I'll include as much documentation here and on the repo's wiki!  I
expect to update this as much as possible to add features as they become available!
Until then, if you run into any bugs let me know!
"""

import os
import ccxt
from strategies import SimpleStrategy
from auth import get_token
from flask import Flask, request, abort
from dotenv import load_dotenv
import ast
import utils

log = utils.getLogger()

load_dotenv()

# Create Flask object called app.
app = Flask(__name__)

# Init ccxt client
API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')

exchange = ccxt.bybit({
    'verbose': False,
    'enableRateLimit': True,
    'apiKey': API_KEY,
    'secret': API_SECRET,
    "options": {'defaultType': 'swap'}, # Choose market type spot/future see https://docs.ccxt.com/en/latest/manual.html#market-structure
})
# Fetch and load markets in memory
exchange.load_markets()

# Create root to easily let us know its on/working.
@app.route('/')
def root():
    return 'online'

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        # Parse the string data from tradingview into a python dict
        data = parse_webhook(request.get_data(as_text=True))
        # Check that the key is correct
        if get_token() == data['key']:
            log.info(f'POST Received: {data}')
            SimpleStrategy.process(exchange, data)
            return '', 200
        else:
            abort(403)
    else:
        abort(400)

def parse_webhook(webhook_data):

    """
    This function takes the string from tradingview and turns it into a python dict.
    :param webhook_data: POST data from tradingview, as a string.
    :return: Dictionary version of string.
    """
    log.info(f'Raw data recieved: {webhook_data}')
    data = ast.literal_eval(webhook_data)
    return data

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5000)