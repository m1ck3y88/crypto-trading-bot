from connectors.coinbasepro_products import *

if __name__ == '__main__':

    # Live Account Limit Buy/Limit Sell Algorithm
    cur = 'USD'
    spcl_assts = ['SHIB', 'VTHO', 'SPELL', 'SHPING', 'ASM']
    buy_price = float(input("Please enter the buy price: "))
    stp_dirctn = 'STOP_DIRECTION_STOP_DOWN'
    sell_price = float('{:.3f}'.format(buy_price * 1.025))
    coin = input("Please enter the coin abbreviation for the coin\n"
                 "you are investing in\n"
                 "Example: BTC\n").upper()
    asset_id = '{}-{}'.format(coin,cur)
    min_currency_bal = 1
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
            buy_price = float('{:.3f}'.format(price))
            sell_price = float('{:.3f}'.format(buy_price * 1.025))
            for wallet in coinbase_request('GET', '/api/v3/brokerage/accounts?limit=250', '')['accounts']:
                if wallet['currency'] == cur and float(wallet['available_balance']['value']) >= min_currency_bal and min_currency_bal >= 1:
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
                    # For Cryptocurrency That Doesn't Allow Decimal Sizes
                    # fiat_cur = '{:.3f}'.format(math.floor((float(wallet['available_balance']['value']) / price) -
                    #                            ((float(wallet['available_balance']['value']) / price) * 0.006)))
                    # min_asset_bal = float(fiat_cur)
                    # For Cryptocurrency That Allows Decimal Sizes
                    fiat_cur = '{:.3f}'.format((float(wallet['available_balance']['value']) / price) -
                                                   ((float(wallet['available_balance']['value']) / price) * 0.006))
                    min_asset_bal = float(fiat_cur)
                    # For Market Buy Orders
                    # fiat_cur = '{:.3f}'.format(math.floor(float(wallet['available_balance']['value'])))
                    # min_asset_bal = '{:.3f}'.format((float(wallet['available_balance']['value']) / price) -
                    #                                ((float(wallet['available_balance']['value']) / price) * 0.006))
                    # # print(fiat_cur)
                    print(cur + ' Available: ' + '{:.3f}'.format(float(wallet['available_balance']['value'])))
                    # Limit Buy Order (Max)
                    if coin in spcl_assts:
                        last_buy_ordr = placeLimitOrder(Side.BUY.name, asset_id, fiat_cur, '{:.8}'.format(float(price)))
                    else:
                        last_buy_ordr = placeLimitOrder(Side.BUY.name, asset_id, fiat_cur, str(price))
                    print(last_buy_ordr)
                    # Stop Loss Order (Max)
                    # last_buy_ordr = placeStopOrder(Side.BUY.name, asset_id, fiat_cur, str(price * 0.975), str(price), stp_dirctn)
                    # print(last_buy_ordr)
                    # Limit Buy Order (Choose Amount of Cryptocurrency You Want to Buy)
                    # auth_client.place_limit_order(product_id=asset_id, side='buy', price=str(price),
                    #                               size=str(lmtbuy_asst_amnt))
                    # Market Buy Order
                    # auth_client.place_market_order(product_id=asset_id, side='buy', funds=fiat_cur)
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
                            print(coin + ' Available: ' + '{:.3f}'.format(float(wallet['available_balance']['value'])))
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
            if flld_sell_ordr and not flld_buy_ordr:
                buy_price = float('{:.3f}'.format(price))
                sell_price = float('{:.3f}'.format(buy_price * 1.025))
            elif not flld_buy_ordr and not flld_sell_ordr:
                if not last_buy_ordr:
                    last_buy_ordr = {
                                      "entry_id": "0123456789",
                                      "trade_id": "0123456789",
                                      "order_id": "0123456789",
                                      "trade_time": "0123456789",
                                      "trade_type": "FILL",
                                      "price": "0123456789",
                                      "size": "0123456789",
                                      "commission": "0123456789",
                                      "product_id": "ABC-USD",
                                      "sequence_timestamp": "0123456789",
                                      "liquidity_indicator": "MAKER",
                                      "size_in_quote": False,
                                      "user_id": "fa018cd4-479c-5a78-b676-533726262bb0",
                                      "side": "BUY"
                                    }
                buy_price = float('{:.3f}'.format(price))
                sell_price = float('{:.3f}'.format(buy_price * 1.025))

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
                    if coin == 'MKR':
                        coin_cur = '{:.3f}'.format(float(asset['available_balance']['value']))
                    else:
                        coin_cur = asset['available_balance']['value']
                    print(coin + ' Available: ' + coin_cur)
                    # Limit Sell Order (Choose Amount of Cryptocurrency You Want to Buy)
                    # auth_client.place_limit_order(product_id=asset_id, side='sell', price=str(price),
                    #                               size=str(lmttbuy_asst_amnt))
                    # Limit Sell Order (Max)
                    last_sell_ordr = placeLimitOrder(Side.SELL.name, asset_id, coin_cur, str(price))
                    print(last_sell_ordr)
                    print(f'Buy price: ${str(buy_price)}')
                    print(f'Sell price: ${str(sell_price)}')
                    if delay == 1:
                        print(f'Checking again in {str(delay)} second...')
                    else:
                        print(f'Checking again in {str(delay)} seconds...')
                    print('---------------------------------------------\n')
                    # Market Sell Order
                    # auth_client.place_market_order(product_id=asset_id, side='sell', funds=coin_cur)
                else:
                    if asset['currency'] == cur and float(asset['available_balance']['value']) >= min_currency_bal:
                        print('You\'ve already made a profit\n'
                              'and are waiting to buy back in')
                        print(cur + ' Available: ' + '{:.3f}'.format(float(asset['available_balance']['value'])))
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

    # Sandbox Account Algorithm:
    # sb_cur = 'USD'
    # sb_buy_price = float(input("Please enter the buy price: "))
    # sb_sell_price = float(input("Please enter the sell price: "))
    # sb_coin = input("Please enter the coin abbreviation for the coin\n"
    #                 "you are investing in\n"
    #                 "Example: BTC\n").upper()
    # sb_asset_id = input("Please enter the asset you want to invest in\n"
    #                     "using the following format: asset-currency\n"
    #                     "Example: BTC-USD\n").upper()
    # sb_min_currency_bal = float(input("Please enter minimum balance of your\n"
    #                                   "native currency you choose to have in order to trade: "))
    # sb_min_asset_bal = float(input("Please enter minimum balance of your asset (cryptocurrency)\n"
    #                                "you choose to have in order to trade: "))
    # # sb_lmtbuy_asst_amnt = float(input("Please enter the amount of the asset\n"
    # #                                 "you want to purchase: "))
    # sb_delay = int(input("Please enter the number of seconds you choose to wait before checking\n"
    #                      "to buy/sell again: "))
    # sb_count = 0
    #
    # while True:
    #     price = float(auth_sandbox_client.get_product_ticker(product_id=sb_asset_id)['price'])
    #     if price <= sb_buy_price:
    #         # sb_buy_price = price
    #         for wallet in get_sandbox_accounts():
    #             if wallet['currency'] == sb_cur and float(wallet['available_balance']['value']) >= sb_min_currency_bal:
    #                 print('Buying ' + sb_coin + '!')
    #                 # For Cryptocurrency Worth More Than a Dollar
    #                 fiat_cur = '{:.8f}'.format((float(wallet['available_balance']['value']) / price) -
    #                                            ((float(wallet['available_balance']['value']) / price) * 0.006))
    #                 print(wallet)
    #                 # sb_lmtbuy_asst_amnt = '{:.3f}'.format(math.floor(float(fiat_cur)/sb_buy_price))
    #                 # print('Currency balance converted to cryptocurrency: ' + sb_lmtbuy_asst_amnt)
    #                 print(sb_cur + ' Available: ' + '{:.3f}'.format(float(wallet['available_balance']['value'])))
    #                 auth_sandbox_client.place_limit_order(product_id=sb_asset_id, side='buy', price=str(price),
    #                                               size=fiat_cur)
    #                 # auth_sandbox_client.place_limit_order(product_id=sb_asset_id, side='buy', price=str(price),
    #                 #                               size=str(sb_lmtbuy_asst_amnt))
    #                 # auth_sandbox_client.place_market_order(product_id=sb_asset_id, side='buy', funds=fiat_cur)
    #                 if sb_delay == 1:
    #                     print(f'Checking again in {str(sb_delay)} second...')
    #                 else:
    #                     print(f'Checking again in {str(sb_delay)} seconds...')
    #                 print('---------------------------------------------\n')
    #             else:
    #                 if wallet['currency'] == sb_coin and float(wallet['available_balance']['value']) >= sb_min_asset_bal:
    #                     if sb_count == 0:
    #                         print('Your\'re already invested in ' + sb_coin + '!')
    #                         print(sb_coin + ' Available: ' + '{:.3f}'.format(float(wallet['available_balance']['value'])))
    #                         if sb_delay == 1:
    #                             print(f'Checking again in {str(sb_delay)} second...')
    #                         else:
    #                             print(f'Checking again in {str(sb_delay)} seconds...')
    #                         print('---------------------------------------------\n')
    #                         sb_count += 1
    #                     else:
    #                         print('The market is trending downwards')
    #                         if sb_delay == 1:
    #                             print(f'Checking again in {str(sb_delay)} second...')
    #                         else:
    #                             print(f'Checking again in {str(sb_delay)} seconds...')
    #                         print('---------------------------------------------\n')
    #
    #     elif price >= sb_sell_price:
    #         for asset in get_sandbox_accounts():
    #             if asset['currency'] == sb_coin and float(asset['available_balance']['value']) >= sb_min_asset_bal:
    #                 print('You made a profit! Selling ' + sb_coin + '!')
    #                 # '{:.3f}'.format(math.floor(float(asset['available_balance']['value'])))
    #                 # '{:.3f}'.format(float(asset['available_balance']['value']))
    #                 coin_cur = asset['available_balance']['value']
    #                 print(sb_coin + ' Available: ' + coin_cur)
    #                 # auth_sandbox_client.place_limit_order(product_id=sb_asset_id, side='sell', price=str(sb_sell_price),
    #                 #                               size=str(sb_lmtbuy_asst_amnt))
    #                 auth_sandbox_client.place_limit_order(product_id=sb_asset_id, side='sell', price=str(price), size=coin_cur)
    #                 # auth_sandbox_client.place_market_order(product_id=sb_asset_id, side='sell', funds=coin_cur)
    #             else:
    #                 if asset['currency'] == sb_cur and float(asset['available_balance']['value']) >= sb_min_currency_bal:
    #                     print('You\'ve already made a profit\n'
    #                           'and are waiting to buy back in')
    #                     print(sb_cur + ' Available: ' + '{:.3f}'.format(float(asset['available_balance']['value'])))
    #                     if sb_delay == 1:
    #                         print(f'Checking again in {str(sb_delay)} second...')
    #                     else:
    #                         print(f'Checking again in {str(sb_delay)} seconds...')
    #                     print('---------------------------------------------\n')
    #
    #     else:
    #         print('\nThe market is trending upwards but\n'
    #               'you either haven\'t bought in yet or you\'ve\n'
    #               'bought in and the market price hasn\'t reached\n'
    #               'your target sell price yet')
    #         if sb_delay == 1:
    #             print(f'Checking again in {str(sb_delay)} second...')
    #         else:
    #             print(f'Checking again in {str(sb_delay)} seconds...')
    #         print('---------------------------------------------\n')
    #     time.sleep(sb_delay)