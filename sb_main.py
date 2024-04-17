from connectors.sb_coinbasepro_products import *

if __name__ == '__main__':

    # Live Account Limit Buy/Limit Sell Algorithm
    cur = 'USD'
    spcl_assts = ['SHIB', 'BONK', 'VTHO', 'SPELL', 'SHPING']
    buy_price = float(input("Please enter the buy price: "))
    # stp_dirctn = 'STOP_DIRECTION_STOP_DOWN'
    price_dec_plcs = 2
    amnt_dec_plcs = 3
    prc_mltplr = 1.025
    sll_prc_divdr = 0.00625
    sell_price = float(('{:.' + str(price_dec_plcs) + 'f}').format(buy_price * (prc_mltplr)))
    coin = input("Please enter the coin abbreviation for the coin\n"
                 "you are investing in\n"
                 "Example: BTC\n").upper()
    asset_id = '{}-{}'.format(coin,cur)
    # set_usd_accnt_bal = 602.00
    min_currency_bal = 2
    min_asset_bal = 1
    delay = int(input("Please enter the number of seconds you choose to wait before checking\n"
                      "to buy/sell again: "))
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
            elif last_sell_ordr and order['order_id'] == last_sell_ordr['order_id']:
                flld_sell_ordr = order
            
        if price <= buy_price:
            if price < buy_price:
                buy_price = float(('{:.' + str(price_dec_plcs) + 'f}').format(price))
                sell_price = float(('{:.' + str(price_dec_plcs) + 'f}').format(buy_price * prc_mltplr))
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
                    # For Set Amount Of Cryptocurrency That Doesn't Allow Decimal Sizes
                    # fiat_cur = ''
                    # if wallet['available_balance']['value'] > set_usd_accnt_bal:
                    #     fiat_cur = '{:.2f}'.format(math.floor((float(set_usd_accnt_bal/ price) -
                    #                                ((set_usd_accnt_bal / price) * 0.0025))))
                    # else:
                    #     break
                    # min_asset_bal = float(fiat_cur)

                    # For Set Amount Of Cryptocurrency That Allows Decimal Sizes
                    # fiat_cur = ('{:.' + str(price_dec_plcs) + 'f}').format((float(set_usd_accnt_bal/ price)
                    #                                - ((set_usd_accnt_bal / price) * 0.0025)))
                    # min_asset_bal = float(fiat_cur)

                    # For Cryptocurrency That Doesn't Allow Decimal Sizes
                    # fiat_cur = ('{:.' + str(price_dec_plcs) + 'f}').format(math.floor((float(wallet['available_balance']['value']) / price) -
                    #                            (float(wallet['available_balance']['value']) / price * 0.0025)))
                    # min_asset_bal = float(fiat_cur)

                    # For Cryptocurrency That Allows Decimal Sizes
                    # fiat_cur = ('{:.' + str(amnt_dec_plcs) + 'f}').format((float(wallet['available_balance']['value']) / price)) 
                    #                            -((float(wallet['available_balance']['value']) / price) * 0.0025))
                    # min_asset_bal = float(fiat_cur)

                    # For Market Buy Orders That Allow Decimal Sizes
                    fiat_cur = ('{:.' + str(price_dec_plcs) + 'f}').format(float(wallet['available_balance']['value']))
                    # min_asset_bal = fiat_cur
    
                    # Limit Buy Order (Max)
                    # if coin in spcl_assts:
                    #     last_buy_ordr = placeLimitOrder(Side.BUY.name, asset_id, fiat_cur,  '{:.8f}'.format(price))
                    # else:
                    #     last_buy_ordr = placeLimitOrder(Side.BUY.name, asset_id, fiat_cur, str(price))
                    
                    # Stop Loss Order (Max)
                    # last_buy_ordr = placeStopOrder(Side.BUY.name, asset_id, fiat_cur, str(price * 0.975), str(price), stp_dirctn)

                    # Limit Buy Order (Choose Amount of Cryptocurrency You Want to Buy)
                    # auth_client.place_limit_order(product_id=asset_id, side='buy', price=str(price),
                    #                               size=str(lmtbuy_asst_amnt))

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
                buy_price = float(('{:.' + str(price_dec_plcs) + 'f}').format(price - (price * sll_prc_divdr)))
                sell_price = float(('{:.' + str(price_dec_plcs) + 'f}').format(buy_price * prc_mltplr))

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

                    #For Market Orders That Don't Allow Decimal Values
                    # coin_cur = ('{:.2f}').format(math.floor(float(asset['available_balance']['value'])))

                    #For Market Orders That Allow Decimal Values
                    coin_cur = ('{:.' + str(amnt_dec_plcs) + 'f}').format(float(asset['available_balance']['value']))

                    # For Cryptocurrency That Allows Decimal Values
                    # coin_cur = ('{:.2f}').format(float(asset['available_balance']['value'])) -
                    #                            (float(asset['available_balance']['value']) * 0.0025))

                    # For Cryptocurrency That Doesn't Allow Decimal Values
                    # coin_cur = ('{:.2f}').format(math.floor(float(asset['available_balance']['value'])))

                    # Limit Sell Order (Max)
                    # last_sell_ordr = placeLimitOrder(Side.SELL.name, asset_id, coin_cur, str(price))

                    # Market Sell Order
                    last_sell_ordr = placeMarketSellOrder(Side.BUY.name, asset_id, coin_cur)

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

    