from pprint import pprint

def close_all_on_symbol(exchange, symbol):
    print('===================')
    print('Close all positions for', symbol)
    print('===================')
    positions = exchange.fetch_positions()
    for pos in positions:
        if pos['future'] == symbol and pos['entryPrice'] != None: 
                pprint(pos)
                print('Ok close position for', symbol)
                closeOrder = exchange.createOrder(pos['future'], 'market', 'buy' if pos['side']=='sell' else 'sell', pos['openSize'])
                print("Close order result:", closeOrder)
