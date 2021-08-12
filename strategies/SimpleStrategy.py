import os
import ccxt
import ast
from pprint import pprint
import utils

STRATEGY_NAME='simple-strategy'

def process(data):
    """
    This function apply simple strategy of buy/sell at tradingview alert signal.
    First close all open positions on the symbole then buy or sell order to FTX.
    :param data: python dict, with keys as the API parameters.
    :return: the response from the exchange.
    """
    # Check if is the right strategy
    if 'strategy' not in data or data['strategy'] != STRATEGY_NAME :
        print('Skip this is not the', STRATEGY_NAME)
        return 

    API_KEY = os.getenv('API_KEY')
    API_SECRET = os.getenv('API_SECRET')
    SUBACCOUNT = data['subAccount'] if 'subAccount' in data else os.getenv('DEFAULT_SUBACCOUNT')
    
    exchange = ccxt.ftx({
        'enableRateLimit': True,
        'apiKey': API_KEY,
        'secret': API_SECRET,
        'headers': {
            'FTX-SUBACCOUNT': SUBACCOUNT,
        },
    })

    # Percent of balance used
    percentBalance = float(os.getenv('PERCENT_BALANCE'))

    # Map symbol to FTX symbol
    symbol = data['symbol']
    symbol = symbol[0:symbol.index('PERP')] + '-PERP'
    # Balance
    funds = exchange.fetchBalance()
    balanceFreeUSD = funds['USD']['free']
    print('USD balance free:', balanceFreeUSD)
    # Current symbol market prices
    ask = float(exchange.markets[symbol]['info']['ask'])
    bid = float(exchange.markets[symbol]['info']['bid'])
    print("ask:", ask, " bid:", bid, " spread:", (ask-bid))
    amountInUSD = round(balanceFreeUSD * (percentBalance/100), 4)
    # Use leverage ?
    if 'useLeverage' in data and data['useLeverage'] == 'true':
        # Get account leverage
        account = exchange.privateGetAccount()
        leverage = account['result']['leverage']
        print("Use leverage:", leverage)
        amountInUSD *= float(leverage)
    
    print("AmoundInUSD:", amountInUSD)

    # Close all positions for the symbol
    utils.close_all_on_symbol(exchange, symbol)

    print('==============')
    print('Open position')
    print('==============')
    # Create order
    type = data['type']
    side = data['side']
    amount = round(amountInUSD/ask, 4)
    print("Amout BTC:", amount)
    order = exchange.createOrder(symbol, type, side, amount)
    print("createOrder:")
    pprint(order)
