from connectors.coinbasepro_products import *
import sys

if __name__ == '__main__':

    # Live Account Limit Buy/Limit Sell Algorithm
    # main()
    cur = 'USD'
    spcl_assts = ['SHIB', 'BONK', 'VTHO', 'SPELL', 'SHPING']
    # float(input("Please enter the buy price: "))
    # stp_dirctn = 'STOP_DIRECTION_STOP_DOWN'
    price_dec_plcs = int(sys.argv[1])
    amnt_dec_plcs = int(sys.argv[2])
    sell_price_mltplr = float(sys.argv[3])
    buy_price_divdr = float(sys.argv[4])
    coin = sys.argv[5].upper()
    # input("Please enter the coin abbreviation for the coin\n"
    #              "you are investing in\n"
    #              "Example: BTC\n").upper()
    asset_id = '{}-{}'.format(coin,cur)
    orig_buy_price = float(getProductInfo(asset_id)['price'])
    buy_price = orig_buy_price
    sell_price = float(('{:.' + str(price_dec_plcs) + 'f}').format(buy_price * (sell_price_mltplr)))
    # set_usd_accnt_bal = 602.00
    min_currency_bal = 10
    min_asset_bal = 0.1

    """
    ONE   => LIMIT REG NO DEC
    TWO   => LIMIT TAKER NO DEC
    THREE => LIMIT REG DEC
    FOUR  => LIMIT TAKER DEC
    FIVE  => MARKET REG NO DEC
    SIX   => MARKET TAKER NO DEC
    SEVEN => MARKET REG DEC
    EIGHT => MARKET TAKER DEC

    """
    buy_order_type = sys.argv[6].upper()
    sell_order_type = sys.argv[7].upper()
    select_limit_buy_order = sys.argv[8]
    select_limit_sell_order = sys.argv[9]

    delay = int(sys.argv[10])
    count = 0
    fee = 0.0041
    # float(input("Enter fee percentage.\nExample: 0.0025\n"))
    # int(input("Please enter the number of seconds you choose to wait before checking\n"
    #                   "to buy/sell again: "))
    last_buy_ordr = {}
    last_sell_ordr = {}
    flld_buy_ordr = {}
    flld_sell_ordr = {}    

    if select_limit_buy_order in ['true', 'false'] and select_limit_buy_order == 'true':
        select_limit_buy_order = True
    else:
        select_limit_buy_order = False

    if select_limit_sell_order in ['true', 'false'] and select_limit_sell_order == 'true':
        select_limit_sell_order = True
    else:
        select_limit_sell_order = False

    while True:
        
        price = float(getProductInfo(asset_id)['price'])
            
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

                    """
                    ONE   => LIMIT REG NO DEC
                    TWO   => LIMIT TAKER NO DEC
                    THREE => LIMIT REG DEC
                    FOUR  => LIMIT TAKER DEC
                    FIVE  => MARKET REG NO DEC
                    SIX   => MARKET TAKER NO DEC
                    SEVEN => MARKET REG DEC
                    EIGHT => MARKET TAKER DEC

                    """

                    if buy_order_type == 'ONE':
                        # For Limit Buy Orders That Don't Allow Decimal Sizes
                        fiat_cur = '{:.2f}'.format(math.floor((float(wallet['available_balance']['value']) / price)))
                        # min_asset_bal = float(fiat_cur)
                    elif buy_order_type == 'TWO':
                        # For Limit Buy Taker Orders That Don't Allow Decimal Sizes                    
                        coin_amount = '{:.2f}'.format(math.floor((float(wallet['available_balance']['value']) / price)))
                        fiat_cur = '{:.2f}'.format(math.floor(float(coin_amount) - (float(coin_amount) * fee)))
                        # min_asset_bal = float(fiat_cur)
                    elif buy_order_type == 'THREE':
                        # For Limit Buy Orders That Allow Decimal Sizes
                        fiat_cur = ('{:.' + str(amnt_dec_plcs) + 'f}').format((float(wallet['available_balance']['value']) / price))
                        # min_asset_bal = float(fiat_cur)
                    elif buy_order_type == 'FOUR':
                        # For Limit Buy Taker Orders That Allow Decimal Sizes                    
                        coin_amount = ('{:.' + str(amnt_dec_plcs) + 'f}').format((float(wallet['available_balance']['value']) / price))
                        fiat_cur = ('{:.' + str(amnt_dec_plcs) + 'f}').format(float(coin_amount) - (float(coin_amount) * fee))
                        # min_asset_bal = float(fiat_cur)
                    elif buy_order_type == 'FIVE':
                        # For Market Buy Orders That Don't Allow Decimal Sizes
                        fiat_cur = '{:.2f}'.format(math.floor(float(wallet['available_balance']['value'])))
                        # min_asset_bal = float(fiat_cur)
                    elif buy_order_type == 'SIX':
                        # For Market Buy Taker Orders That Don't Allow Decimal Sizes
                        fiat_cur = '{:.2f}'.format(math.floor(float(wallet['available_balance']['value']) -
                            (float(wallet['available_balance']['value']) * fee)))
                    elif buy_order_type == 'SEVEN':
                        # For Market Buy Orders That Allow Decimal Sizes
                        fiat_cur = ('{:.' + str(price_dec_plcs) + 'f}').format(float(wallet['available_balance']['value']))
                        # min_asset_bal = float(fiat_cur)
                    elif buy_order_type == 'EIGHT':
                        # For Market Buy Taker Orders That Allow Decimal Sizes
                        fiat_cur = ('{:.' + str(price_dec_plcs) + 'f}').format(float(wallet['available_balance']['value']) -
                            (float(wallet['available_balance']['value']) * fee))

                    if select_limit_buy_order:
                        # Limit Buy Order (Max)
                        if coin in spcl_assts:
                            last_buy_ordr = placeLimitOrder(Side.BUY.name, asset_id, fiat_cur, '{:.8f}'.format(price))
                        else:
                            last_buy_ordr = placeLimitOrder(Side.BUY.name, asset_id, fiat_cur, str(price))
                    elif not select_limit_buy_order:
                        # Market Buy Order
                        last_buy_ordr = placeMarketBuyOrder(Side.BUY.name, asset_id, fiat_cur)
                    
                    # Stop Loss Order (Max)
                    # last_buy_ordr = placeStopOrder(Side.BUY.name, asset_id, fiat_cur, str(price * 0.975), str(price), stp_dirctn)

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

                    """
                    ONE   => REG NO DEC ORDER
                    TWO   => TAKER NO DEC ORDER
                    THREE => REG DEC ORDER
                    FOUR  => TAKER DEC ORDER

                    """

                    if sell_order_type == 'ONE':
                        # For Limit/Market Sell Orders That Don't Allow Decimal Values
                        coin_cur = '{:.2f}'.format(math.floor(float(asset['available_balance']['value'])))
                    elif sell_order_type == 'TWO':
                        # For Limit/Market Sell Taker Orders That Don't Allow Decimal Values
                        asset_amount = '{:.2f}'.format(math.floor(float(asset['available_balance']['value'])))
                        coin_cur = '{:.2f}'.format(math.floor(float(asset_amount) - (float(asset_amount) * fee)))
                    elif sell_order_type == 'THREE':
                        # For Limit/Market Sell Orders That Allow Decimal Values
                        coin_cur = ('{:.' + str(amnt_dec_plcs) + 'f}').format(float(asset['available_balance']['value']))
                    elif sell_order_type == 'FOUR':
                        # For Limit/Market Sell Taker Orders That Allow Decimal Values
                        asset_amount = ('{:.' + str(amnt_dec_plcs) + 'f}').format(float(asset['available_balance']['value']))
                        coin_cur = ('{:.' + str(amnt_dec_plcs) + 'f}').format(float(asset_amount) - (float(asset_amount) * fee))

                    if select_limit_sell_order:
                        # Limit Sell Order (Max)
                        last_sell_ordr = placeLimitOrder(Side.SELL.name, asset_id, coin_cur, str(price))
                    else:
                        # Market Sell Order
                        last_sell_ordr = placeMarketSellOrder(Side.SELL.name, asset_id, coin_cur)

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