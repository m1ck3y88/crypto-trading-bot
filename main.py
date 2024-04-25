from connectors.coinbasepro_products import *
import sys

if __name__ == '__main__':

    # Live Account Limit Buy/Limit Sell Algorithm
    cur = 'USD'
    spcl_assts = ['SHIB', 'BONK', 'VTHO', 'SPELL', 'SHPING']
    buy_price = float(sys.argv[1])
    # float(input("Please enter the buy price: "))
    # stp_dirctn = 'STOP_DIRECTION_STOP_DOWN'
    price_dec_plcs = int(sys.argv[2])
    amnt_dec_plcs = int(sys.argv[3])
    sell_price_mltplr = float(sys.argv[4])
    buy_price_divdr = float(sys.argv[5])
    sell_price = float(('{:.' + str(price_dec_plcs) + 'f}').format(buy_price * (sell_price_mltplr)))
    coin = sys.argv[6].upper()
    # input("Please enter the coin abbreviation for the coin\n"
    #              "you are investing in\n"
    #              "Example: BTC\n").upper()
    asset_id = '{}-{}'.format(coin,cur)
    # set_usd_accnt_bal = 602.00
    min_currency_bal = 10
    min_asset_bal = 1
    delay = int(sys.argv[7])
    # int(input("Please enter the number of seconds you choose to wait before checking\n"
    #                   "to buy/sell again: "))
    last_buy_ordr = {}
    last_sell_ordr = {}
    flld_buy_ordr = {}
    flld_sell_ordr = {}
    count = 0

    while True:
        
        price = float(getProductInfo(asset_id)['price'])

        for order in coinbase_request('GET', '/api/v3/brokerage/orders/historical/fills', '')['fills']:

            if last_buy_ordr and order['order_id'] == last_buy_ordr['order_id']:
                flld_buy_ordr = order

            if last_sell_ordr and order['order_id'] == last_sell_ordr['order_id']:
                flld_sell_ordr = order

        if flld_buy_ordr and flld_buy_ordr['order_type'] == 'MARKET' and float(flld_buy_ordr['average_filled_price']) > buy_price:

                buy_price = float(('{:.' + str(price_dec_plcs) + 'f}').format(float(flld_buy_ordr['average_filled_price'])))

        if flld_sell_ordr and flld_buy_ordr['order_type'] == 'MARKET' and float(flld_buy_ordr['average_filled_price']) < sell_price:

                sell_price = float(('{:.' + str(price_dec_plcs) + 'f}').format(buy_price * (sell_price_mltplr)))
            
        if price <= buy_price:

            for wallet in coinbase_request('GET', '/api/v3/brokerage/accounts?limit=250', '')['accounts']:
                if wallet['currency'] == cur and float(wallet['available_balance']['value']) >= min_currency_bal:
                    if last_buy_ordr and not last_buy_ordr['order_id'] == '0123456789':
                        print(f"There is already a buy order open for {coin}!\nOrder amount: {last_buy_ordr['size']}")
                        print(f'Buy price: ${str(buy_price)}')
                        print(f'Sell price: ${str(sell_price)}')
                        if delay == 1:
                            print(f'Checking again in {str(delay)} second...')
                        else:
                            print(f'Checking again in {str(delay)} seconds...')
                        print('---------------------------------------------\n')
                        break
                    print('Buying ' + coin + '!')

                    # For Limit Buy Orders That Don't Allow Decimal Sizes
                    # fiat_cur = '{:.2f}'.format(math.floor((float(wallet['available_balance']['value']) / price)))
                    # min_asset_bal = float(fiat_cur)

                    # For Limit Buy Taker Orders That Don't Allow Decimal Sizes                    
                    # coin_amount = '{:.2f}'.format(math.floor((float(wallet['available_balance']['value']) / price)))
                    # fiat_cur = '{:.2f}'.format(math.floor(float(coin_amount) - (float(coin_amount) * 0.0025)))
                    # # min_asset_bal = float(fiat_cur)

                    # For Limit Buy Orders That Allow Decimal Sizes
                    # fiat_cur = ('{:.' + str(amnt_dec_plcs) + 'f}').format((float(wallet['available_balance']['value']) / price))
                    # min_asset_bal = float(fiat_cur)

                    # For Limit Buy Taker Orders That Allow Decimal Sizes                    
                    # coin_amount = ('{:.' + str(amnt_dec_plcs) + 'f}').format((float(wallet['available_balance']['value']) / price))
                    # fiat_cur = ('{:.' + str(amnt_dec_plcs) + 'f}').format(float(coin_amount) - (float(coin_amount) * 0.0025))
                    # min_asset_bal = float(fiat_cur)

                    # For Market Buy Orders That Don't Allow Decimal Sizes
                    fiat_cur = ('{:.2f}').format(math.floor(float(wallet['available_balance']['value'])))
                    # min_asset_bal = float(fiat_cur)

                    # For Market Buy Orders That Allow Decimal Sizes
                    # fiat_cur = ('{:.' + str(price_dec_plcs) + 'f}').format(float(wallet['available_balance']['value']))
                    # min_asset_bal = float(fiat_cur)

                    # Limit Buy Order (Max)
                    # if coin in spcl_assts:
                    #     last_buy_ordr = placeLimitOrder(Side.BUY.name, asset_id, fiat_cur, '{:.8f}'.format(price))
                    # else:
                    #     last_buy_ordr = placeLimitOrder(Side.BUY.name, asset_id, fiat_cur, str(price))
                    
                    # Stop Loss Order (Max)
                    # last_buy_ordr = placeStopOrder(Side.BUY.name, asset_id, fiat_cur, str(price * 0.975), str(price), stp_dirctn)

                    # Market Buy Order
                    last_buy_ordr = placeMarketBuyOrder(Side.BUY.name, asset_id, fiat_cur)

                    print(last_buy_ordr)
                    print(f'Buy price: ${str(buy_price)}')
                    print(f'Sell price: ${str(sell_price)}')
                    if delay == 1:
                        print(f'Checking again in {str(delay)} second...')
                    else:
                        print(f'Checking again in {str(delay)} seconds...')
                    print('---------------------------------------------\n')
                else:
                    if wallet['currency'] == coin and float(wallet['available_balance']['value']) >= min_asset_bal:
                        if count == 0:
                            print('Your\'re already invested in ' + coin + '!')
                            print(coin + ' Available: ' + '{:.2f}'.format(float(wallet['available_balance']['value'])))
                            print(f'Buy price: ${str(buy_price)}')
                            print(f'Sell price: ${str(sell_price)}')
                            if delay == 1:
                                print(f'Checking again in {str(delay)} second...')
                            else:
                                print(f'Checking again in {str(delay)} seconds...')
                            print('---------------------------------------------\n')
                            count += 1
                        else:
                            print('The market is trending downwards')
                            print(f'Buy price: ${str(buy_price)}')
                            print(f'Sell price: ${str(sell_price)}')
                            if delay == 1:
                                print(f'Checking again in {str(delay)} second...')
                            else:
                                print(f'Checking again in {str(delay)} seconds...')
                            print('---------------------------------------------\n')

        elif price >= sell_price:
            # if not last_buy_ordr:
            #     last_buy_ordr = {
            #                         "entry_id": "0123456789",
            #                         "trade_id": "0123456789",
            #                         "order_id": "0123456789",
            #                         "trade_time": "0123456789",
            #                         "trade_type": "FILL",
            #                         "price": "0123456789",
            #                         "size": "0123456789",
            #                         "commission": "0123456789",
            #                         "product_id": "ABC-USD",
            #                         "sequence_timestamp": "0123456789",
            #                         "liquidity_indicator": "MAKER",
            #                         "size_in_quote": False,
            #                         "user_id": "fa018cd4-479c-5a78-b676-533726262bb0",
            #                         "side": "BUY"
            #                     }
            if price > sell_price:
                buy_price = float(('{:.' + str(price_dec_plcs) + 'f}').format(price - (price * buy_price_divdr)))
                sell_price = float(('{:.' + str(price_dec_plcs) + 'f}').format(buy_price * sell_price_mltplr))

            for asset in coinbase_request('GET', '/api/v3/brokerage/accounts?limit=250', '')['accounts']:
                if asset['currency'] == coin and float(asset['available_balance']['value']) >= min_asset_bal:
                    if last_sell_ordr and not last_sell_ordr['order_id'] == '0123456789':
                        print(f"There is already a buy order open for {coin}!\nOrder amount: {last_sell_ordr['size']}")
                        print(f'Buy price: ${str(buy_price)}')
                        print(f'Sell price: ${str(sell_price)}')
                        if delay == 1:
                            print(f'Checking again in {str(delay)} second...')
                        else:
                            print(f'Checking again in {str(delay)} seconds...')
                        print('---------------------------------------------\n')
                    else:
                        print('You made a profit! Selling ' + coin + '!')

                    # For Limit Sell Orders That Don't Allow Decimal Values
                    # coin_cur = '{:.2f}'.format(math.floor(float(asset['available_balance']['value'])))

                    # For Limit Sell Orders That Allow Decimal Values
                    coin_cur = ('{:.' + str(amnt_dec_plcs) + 'f}').format(float(asset['available_balance']['value']))

                    # Limit Sell Order (Max)
                    last_sell_ordr = placeLimitOrder(Side.SELL.name, asset_id, coin_cur, str(price))

                    # Market Sell Order
                    # last_sell_ordr = placeMarketSellOrder(Side.BUY.name, asset_id, coin_cur)

                    print(coin + ' Available: ' + coin_cur)
                    print(last_sell_ordr)
                    print(f'Buy price: ${str(buy_price)}')
                    print(f'Sell price: ${str(sell_price)}')
                    if delay == 1:
                        print(f'Checking again in {str(delay)} second...')
                    else:
                        print(f'Checking again in {str(delay)} seconds...')
                    print('---------------------------------------------\n')
                    
                else:
                    if asset['currency'] == cur and float(asset['available_balance']['value']) >= min_currency_bal:
                        print('You\'ve already made a profit\n'
                              'and are waiting to buy back in')
                        print(cur + ' Available: ' + ('{:.2f}').format(float(asset['available_balance']['value'])))
                        print(f'Buy price: ${str(buy_price)}')
                        print(f'Sell price: ${str(sell_price)}')
                        if delay == 1:
                            print(f'Checking again in {str(delay)} second...')
                        else:
                            print(f'Checking again in {str(delay)} seconds...')
                        print('---------------------------------------------\n')

        else:
            print('\nThe market is trending upwards but\n'
                  'you either haven\'t bought in yet \n'
                 f'(buy price: ${str(buy_price)}) or you\'ve bought\n'
                  'in and the market price hasn\'t reached your\n'
                 f'target sell price yet (sell price: ${str(sell_price)})')
            if delay == 1: 
                print(f'Checking again in {str(delay)} second...')
            else:
                print(f'Checking again in {str(delay)} seconds...')
            print('---------------------------------------------\n')
        time.sleep(delay)