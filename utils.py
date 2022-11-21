import logging

logging.basicConfig(
    format='%(asctime)s.%(msecs)03d %(levelname)-4s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d,%H:%M:%S')

log = logging.getLogger()

def getLogger():
    return log

def close_all_positions_on_symbol(exchange, symbol):
    log.info(f'Close all positions for {symbol}')
    positions = exchange.fetch_positions()
    for pos in positions:
        if pos['symbol'] == symbol and pos['entryPrice'] != None:
            log.info(f'Close position for {symbol}')
            closeOrder = exchange.createOrder(symbol, 
                'market', 
                'buy' if pos['info']['side'] =='Sell' else 'sell', 
                pos['info']['size'],
                params={ 'position_idx': 0, 'reduceOnly': True})
            log.info('Done.')

def close_all_orders_on_symbol(exchange, symbol):
    log.info(f'Close all orders for {symbol}')
    exchange.cancelAllOrders(symbol)
    log.info('Done.')

def get_active_orders_on_symbol(exchange, market):
    log.info(f'Get active orders for {market}')
    #/private/linear/order/list
    params = { 'symbol': market, 'order_status': 'Created,New'}
    return exchange.privateGetPrivateLinearOrderList(params)['result']['data']