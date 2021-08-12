"""
Tradingview-webhooks-bot is a python bot that works with tradingview's webhook alerts!
This bot is not affiliated with tradingview and was created by @robswc

You can follow development on github at: github.com/robswc/tradingview-webhook-bot

I'll include as much documentation here and on the repo's wiki!  I
expect to update this as much as possible to add features as they become available!
Until then, if you run into any bugs let me know!
"""

from strategies import SimpleStrategy
from auth import get_token
from flask import Flask, request, abort
from dotenv import load_dotenv
import ast

load_dotenv()

# Create Flask object called app.
app = Flask(__name__)

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
            print('POST Received:', data)
            SimpleStrategy.process(data)
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
    print("Raw data recieved:", webhook_data)
    data = ast.literal_eval(webhook_data)
    return data

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)