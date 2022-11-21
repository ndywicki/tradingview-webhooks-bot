import os
import ast
import utils

STRATEGY_NAME='simple-strategy'

log = utils.getLogger()

def process(exchange, data):
    """
    This function apply simple strategy of buy/sell at tradingview alert signal.
    First close all open positions on the symbole then buy or sell order to FTX.
    :param data: python dict, with keys as the API parameters.
    :return: the response from the exchange.
    """
    # Check if is the right strategy
    if 'strategy' not in data or data['strategy'] != STRATEGY_NAME :
        log.info(f'Skip this is not the {STRATEGY_NAME}')
        return

    # Check input params
    if data['type'] == 'limit':
        if 'price' not in data:
            log.error('Requires a price argument for limit orders')
            return

    # Percent of balance used
    percentBalance = float(os.getenv('PERCENT_BALANCE'))

    # Get the market & symbol
    market = data['market']
    symbol = exchange.safe_symbol(market)
    log.info(f'Market: {market} symbol: {symbol}')
    minPriceSize = float(exchange.markets[symbol]['info']['lot_size_filter']['min_trading_qty'])
    precision = float(exchange.markets[symbol]['info']['lot_size_filter']['qty_step'])

    # Get current ticker data
    ticker = exchange.fetch_ticker(symbol)

    # Balance
    funds = exchange.fetchBalance()
    balanceFreeUSD = funds['USDT']['free']
    log.info(f'USD balance free: {balanceFreeUSD}')
    # Current market prices
    ask = float(ticker['ask'])
    bid = float(ticker['bid'])
    log.info(f'ask: {ask} bid: {bid} spread: {ask-bid}')
    amountInUSD = round(balanceFreeUSD * (percentBalance/100), 4)

    # # Use leverage? (not available on SPOT markets)
    if 'useLeverage' in data and data['useLeverage'] == 'true':
        # Get leverage by fetching position, even if no positions, bybit return dummy pos...
        positions = exchange.fetch_positions()
        leverage = positions[0]['info']['leverage']
        log.info(f'Use leverage: {leverage}')
        amountInUSD *= float(leverage)

    log.info(f'AmoundInUSD: {amountInUSD}')

    activeOrders = utils.get_active_orders_on_symbol(exchange, market)
    # Close all active orders for the symbol
    if activeOrders:
        utils.close_all_orders_on_symbol(exchange, symbol)
    # Close all positions & pending orders for the symbol
    utils.close_all_positions_on_symbol(exchange, symbol)

    log.info('Open position.')
    # Create order
    type = data['type']
    side = data['side']
    price = None
    if type == 'limit':
        price = float(data['price'])
    amount = round(amountInUSD/ask, 4) if round(amountInUSD/ask, 4) > minPriceSize else minPriceSize
    log.info(f'Amount for {symbol} : {amount}')
    params = { 'position_idx': 0}
    order = exchange.createOrder(symbol, type, side, amount, price, params)
    log.info(f"createOrder id: {order['id']}")