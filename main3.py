from connectors.coinbasepro_products import *
import time
import sys

if __name__ == '__main__':

    # Live Account Limit Buy/Limit Sell Algorithm
    cur = 'USD'
    txt_filename = 'bot_cmd_line_setup_with_manual_buy_sell_price_entry.txt'
    json_filename = 'all_accounts_[Nov_28_2025].json'
    all_accounts = get_all_assets(json_filename)
    usd_wallet = [wallet for wallet in all_accounts if wallet['currency'] == cur][0]
    asset_args = get_asset_args_setup(get_assets_args_setup_list(txt_filename), sys.argv[1])
    spcl_assts = ['SHIB', 'BONK', 'VTHO', 'SPELL', 'SHPING']
    buy_price = float(sys.argv[2])
    price_dec_plcs = int(asset_args[3])
    amnt_dec_plcs = int(asset_args[4])
    sell_price_mltplr = float(sys.argv[3])
    buy_price_divdr = float(sys.argv[4])
    sell_price = float(('{:.' + str(price_dec_plcs) + 'f}').format(buy_price * (sell_price_mltplr)))
    coin = sys.argv[1].upper()
    coin_wallet = [wallet for wallet in all_accounts if wallet['currency'] == coin][0]
    asset_id = '{}-{}'.format(coin, cur)

    if sys.argv[5] == 'one':
        investment_amount = buy_price
    else:
        investment_amount = float(sys.argv[5])

    coin_amount = float(('{:.' + str(amnt_dec_plcs) + 'f}').format(investment_amount / buy_price))
    remainder = 0.00
    # maker_fee = 0.0025
    # fee = 0.0040
    min_currency_bal = float(sys.argv[6])
    unique_identifier = str(uuid.uuid1())[:8]

    '''
    ONE   => LIMIT REG NO DEC
    TWO   => LIMIT TAKER NO DEC
    THREE => LIMIT REG DEC
    FOUR  => LIMIT TAKER DEC
    FIVE  => MARKET REG NO DEC
    SIX   => MARKET TAKER NO DEC
    SEVEN => MARKET REG DEC
    EIGHT => MARKET TAKER DEC

    '''
    buy_order_type = sys.argv[7].upper()
    sell_order_type = sys.argv[8].upper()
    select_limit_buy_order = sys.argv[9].lower()
    select_limit_sell_order = sys.argv[10].lower()

    size = 0.0

    # delay_list = [1, 5, 10, 15, 20, 30, 60, 120, 150, 300, 600, 900, 1800, 3600]
    delay = float(sys.argv[11])
    count = 0 # float(sys.argv[12])

    last_buy_ordr = {}
    last_sell_ordr = {}

    if select_limit_buy_order == 'true':
        select_limit_buy_order = True
    else:
        select_limit_buy_order = False

    if select_limit_sell_order == 'true':
        select_limit_sell_order = True
    else:
        select_limit_sell_order = False

    prefill_buy_order_list = []
    filled_buy_order_list = [] # This list is for preparing sell orders and keeping record of buy orders with no matching sell order

    while True:

        price = float(client.get_product(asset_id).to_dict()['price'])

        # delay = delay_list[randint(0, len(delay_list) - 1)]
        if len(prefill_buy_order_list) >= 1:
            for idx, order in enumerate(prefill_buy_order_list):
                order_info = check_if_order_filled(order)
                filled = order_info[0]

                if filled:
                    filled_buy_order_list.append(order_info[1])
                    prefill_buy_order_list.pop(idx)
                elif filled == None:
                    print('Order cancelled!')
                    prefill_buy_order_list.pop(idx)

        file_path = f'flld_buy_ordrs_{asset_id}_main3[{dt.now().strftime("%b_%d_%Y")}]{unique_identifier}.txt'

        with open(file_path, 'w') as file:
            file.write(str(filled_buy_order_list))

        if price <= buy_price:

            if price < buy_price:
                buy_price = float(('{:.' + str(price_dec_plcs) + 'f}').format(price))
                sell_price = float(('{:.' + str(price_dec_plcs) + 'f}').format(buy_price * (sell_price_mltplr)))

            wallet = client.get_account(account_uuid=usd_wallet['uuid']).to_dict()['account']

            if float(wallet['available_balance']['value']) >= min_currency_bal:
                    
                if float(wallet['available_balance']['value']) >= (investment_amount + 2):
                    remainder = float(wallet['available_balance']['value']) - investment_amount
                # else:
                #     investment_amount = float(wallet['available_balance']['value'])

                print('Buying ' + coin + '!')

                '''
                ONE   => LIMIT REG NO DEC
                TWO   => LIMIT TAKER NO DEC
                THREE => LIMIT REG DEC
                FOUR  => LIMIT TAKER DEC
                FIVE  => MARKET REG NO DEC
                SIX   => MARKET TAKER NO DEC
                SEVEN => MARKET REG DEC
                EIGHT => MARKET TAKER DEC
            
                '''

                best_bid = float(client.get_best_bid_ask(product_ids=[asset_id]).to_dict()['pricebooks'][0]['bids'][0]['price'])

                if sys.argv[5] == 'one':
                    investment_amount = best_bid

                if buy_order_type == 'ONE':
                    # For Limit Buy Orders That Don't Allow Decimal Sizes
                    fiat_cur = '{:.2f}'.format(math.floor(investment_amount / best_bid))
                elif buy_order_type == 'TWO':
                    # For Limit Buy Taker Orders That Don't Allow Decimal Sizes                    
                    coin_amnt = '{:.2f}'.format(math.floor(investment_amount / best_bid))
                    fiat_cur = coin_amnt
                elif buy_order_type == 'THREE':
                    # For Limit Buy Orders That Allow Decimal Sizes
                    fiat_cur = ('{:.' + str(amnt_dec_plcs) + 'f}').format(investment_amount / best_bid)
                elif buy_order_type == 'FOUR':
                    # For Limit Buy Taker Orders That Allow Decimal Sizes                    
                    coin_amnt = ('{:.' + str(amnt_dec_plcs) + 'f}').format(investment_amount / best_bid)
                    fiat_cur = coin_amnt
                elif buy_order_type == 'FIVE':
                    # For Market Buy Orders That Don't Allow Decimal Sizes
                    fiat_cur = '{:.2f}'.format(math.floor(investment_amount))
                    # size = math.floor(float(('{:.' + str(amnt_dec_plcs) + 'f}').format(float(fiat_cur) - (float(fiat_cur) / price))))
                elif buy_order_type == 'SIX':
                    # For Market Buy Taker Orders That Don't Allow Decimal Sizes
                    fiat_cur = '{:.2f}'.format(math.floor(investment_amount))
                elif buy_order_type == 'SEVEN':
                    # For Market Buy Orders That Allow Decimal Sizes
                    fiat_cur = ('{:.' + str(price_dec_plcs) + 'f}').format(investment_amount)
                    # size = float(('{:.' + str(amnt_dec_plcs) + 'f}').format(float(fiat_cur) - (float(fiat_cur) / price)))
                elif buy_order_type == 'EIGHT':
                    # For Market Buy Taker Orders That Allow Decimal Sizes
                    fiat_cur = ('{:.' + str(price_dec_plcs) + 'f}').format(investment_amount)

                if select_limit_buy_order:
                    # Limit Buy Order (Max)
                    if coin in spcl_assts:
                        last_buy_ordr = client.limit_order_gtc_buy(client_order_id=str(generate_client_order_id()),product_id=asset_id,base_size=fiat_cur,limit_price=('{:.' + str(price_dec_plcs) + 'f}').format(best_bid))

                        prefill_buy_order_list.append(last_buy_ordr)
                        
                        with open(f'[{dt.now().strftime("%b_%d_%Y")}]last_buy_order.json', 'w') as file:

                            json.dump(last_buy_ordr.to_dict(), file, indent=6)
                    else:
                        last_buy_ordr = client.limit_order_gtc_buy(client_order_id=str(generate_client_order_id()),product_id=asset_id,base_size=fiat_cur,limit_price=str(best_bid))

                        prefill_buy_order_list.append(last_buy_ordr)

                        with open(f'[{dt.now().strftime("%b_%d_%Y")}]last_buy_order.json', 'w') as file:

                            json.dump(last_buy_ordr.to_dict(), file, indent=6)

                elif not select_limit_buy_order:
                    # Market Buy Order
                    last_buy_ordr = client.market_order_buy(client_order_id=str(generate_client_order_id()), product_id=asset_id, quote_size=fiat_cur)

                    prefill_buy_order_list.append(last_buy_ordr)

                    with open(f'[{dt.now().strftime("%b_%d_%Y")}]last_buy_order.json', 'w') as file:

                        json.dump(last_buy_ordr.to_dict(), file, indent=6)

                # Stop Loss Order (Max)
                # last_buy_ordr = placeStopOrder(Side.BUY.name, asset_id, fiat_cur, str(price * 0.975), str(price), stp_dirctn)

                # print(last_buy_ordr)
                if remainder >= 2:
                    print('\n---------------------------------------------')
                    print(f"You're ${'{:.2f}'.format(remainder)} above your goal!")
                    print(f"Convert ${'{:.2f}'.format(remainder)} to USDC.")
                    print('---------------------------------------------\n')
                print(f'Buy price: ${str(buy_price)}')
                print(f'Sell price: ${str(sell_price)}')
                if delay == 1:
                    print(f'Checking again in {str(delay)} second...')
                else:
                    print(f'Checking again in {str(delay)} seconds...')
                print('---------------------------------------------\n')
            else:
                asst = client.get_account(account_uuid=coin_wallet['uuid']).to_dict()['account']
                if float(asst['available_balance']['value']) >= size and count == 0:
                    print('Your\'re already invested in ' + coin + '!')
                    print(coin + ' Available: ' + '{:.2f}'.format(float(asst['available_balance']['value'])))
                    count += 1    
                if float(wallet['available_balance']['value']) < min_currency_bal:
                    print('---------------------------------------------\n')
                    print('Your account balance is below the minumum required to trade.')
                    print(f'Minimum amount required: ${str(min_currency_bal)}')
                    print(f"Current account balance: ${('{:.' + str(amnt_dec_plcs) + 'f}').format(float(wallet['available_balance']['value']))}")
                    print('\n---------------------------------------------\n')

                if price == buy_price:
                    print('The market is not trending upwards or downwards')
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

            asset = client.get_account(account_uuid=coin_wallet['uuid']).to_dict()['account']

            if price > sell_price:
                buy_price = float(('{:.' + str(price_dec_plcs) + 'f}').format(price - (price * buy_price_divdr)))
                sell_price = float(('{:.' + str(price_dec_plcs) + 'f}').format(buy_price * sell_price_mltplr))

            if len(filled_buy_order_list) >=1:
                print('You made a profit! Selling ' + coin + '!')

                '''
                ONE   => REG NO DEC ORDER
                TWO   => TAKER NO DEC ORDER
                THREE => REG DEC ORDER
                FOUR  => TAKER DEC ORDER

                '''

                if sell_order_type == 'ONE':
                    # For Limit/Market Sell Orders That Don't Allow Decimal Values
                    print(f"Sellng {('{:.' + str(amnt_dec_plcs) + 'f}').format(float(asset['available_balance']['value']))} of {coin}!")
                elif sell_order_type == 'TWO':
                    # For Limit/Market Sell Taker Orders That Don't Allow Decimal Values
                    print(f"Sellng {('{:.' + str(amnt_dec_plcs) + 'f}').format(float(asset['available_balance']['value']))} of {coin}!")
                elif sell_order_type == 'THREE':
                    # For Limit/Market Sell Orders That Allow Decimal Values
                    print(f"Sellng {('{:.' + str(amnt_dec_plcs) + 'f}').format(float(asset['available_balance']['value']))} of {coin}!")
                elif sell_order_type == 'FOUR':
                    # For Limit/Market Sell Taker Orders That Allow Decimal Values
                    print(f"Sellng {('{:.' + str(amnt_dec_plcs) + 'f}').format(float(asset['available_balance']['value']))} of {coin}!")

                for idx, order in enumerate(filled_buy_order_list):

                    if order['order_type'] == 'LIMIT':

                        size = float(order['order_configuration']['limit_limit_gtc']['base_size'])

                        order_price = float(order['order_configuration']['limit_limit_gtc']['limit_price'])

                        order_sell_price = float(('{:.' + str(price_dec_plcs) + 'f}').format(order_price * sell_price_mltplr))

                    elif order['order_type'] == 'MARKET':
                        
                        size = float(order['filled_size'])

                        order_price = float(order['average_filled_price'])

                        order_sell_price = float(('{:.' + str(price_dec_plcs) + 'f}').format(order_price * sell_price_mltplr))

                    if price > order_sell_price:

                        if select_limit_sell_order:
                            # Limit Sell Order (Max)
                            last_sell_ordr = client.limit_order_gtc_sell(client_order_id=str(generate_client_order_id()), product_id=asset_id, base_size=str(size), limit_price= str(price))
                            
                            with open(f'[{dt.now().strftime("%b_%d_%Y")}]last_sell_order.json', 'w') as file:

                                json.dump(last_sell_ordr.to_dict(), file, indent=6)

                        else:
                            # Market Sell Order
                            last_sell_ordr = client.market_order_sell(client_order_id=str(generate_client_order_id()), product_id=asset_id, base_size=str(size))

                            with open(f'[{dt.now().strftime("%b_%d_%Y")}]last_sell_order.json', 'w') as file:

                                json.dump(last_sell_ordr.to_dict(), file, indent=6)
                    else:
                        if select_limit_sell_order:
                            # Limit Sell Order (Max)
                            last_sell_ordr = client.limit_order_gtc_sell(client_order_id=str(generate_client_order_id()), product_id=asset_id, base_size=str(size), limit_price=str(order_sell_price))
                            
                            with open(f'[{dt.now().strftime("%b_%d_%Y")}]last_sell_order.json', 'w') as file:

                                json.dump(last_sell_ordr.to_dict(), file, indent=6)

                        else:
                            # Market Sell Order
                            last_sell_ordr = client.market_order_sell(client_order_id=str(generate_client_order_id()), product_id=asset_id, base_size=str(size))

                            with open(f'[{dt.now().strftime("%b_%d_%Y")}]last_sell_order.json', 'w') as file:

                                json.dump(last_sell_ordr.to_dict(), file, indent=6)
                    filled_buy_order_list.pop(idx)


                print(coin + ' Available: ' + ('{:.' + str(amnt_dec_plcs) + 'f}').format(float(asset['available_balance']['value'])))
                # print(last_sell_ordr)
                print(f'Buy price: ${str(buy_price)}')
                print(f'Sell price: ${str(sell_price)}')
                if delay == 1:
                    print(f'Checking again in {str(delay)} second...')
                else:
                    print(f'Checking again in {str(delay)} seconds...')
                print('---------------------------------------------\n')
            
            else:
                wallet = client.get_account(account_uuid=usd_wallet['uuid']).to_dict()['account']
                if float(wallet['available_balance']['value']) >= min_currency_bal:
                    print('You\'ve already made a profit\n'
                            'and are waiting to buy back in')
                    print(cur + ' Available: ' + ('{:.2f}').format(float(wallet['available_balance']['value'])))
                    print(f'Buy price: ${str(buy_price)}')
                    print(f'Sell price: ${str(sell_price)}')
                    if delay == 1:
                        print(f'Checking again in {str(delay)} second...')
                    else:
                        print(f'Checking again in {str(delay)} seconds...')
                    print('---------------------------------------------\n')
                print('The market is trending upwards but your asset balance\n'
                    'is below the minimum required to trade')
                print('Current ' + coin + ' balance: ' + ('{:.' + str(amnt_dec_plcs) + 'f}').format(float(asset['available_balance']['value'])))
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
        print('The current price is: $' + ('{:.' + str(price_dec_plcs) + 'f}').format(price))
        print('\n---------------------------------------------\n')

        count += 1
        time.sleep(delay)
