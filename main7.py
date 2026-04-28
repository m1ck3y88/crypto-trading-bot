from connectors.coinbasepro_products import *
import sys

if __name__ == '__main__':

    # Live Account Limit Buy/Limit Sell Algorithm
    cur = 'USD'
    txt_filename = 'bot_cmd_line_setup_with_manual_buy_sell_price_entry.txt'
    json_filename = 'all_accounts_[Nov_28_2025].json'
    all_accounts = get_all_assets(json_filename)
    limit_only_market_assets = ['TRU', 'RONIN', 'TIME', 'LOKA', 'RLS', 'THQ']
    usd_wallet = [wallet for wallet in all_accounts if wallet['currency'] == cur][0]
    coin = sys.argv[1].upper()
    asset_id = '{}-{}'.format(coin, cur)
    asset_args = get_asset_args_setup(get_assets_args_setup_list(txt_filename), sys.argv[1])
    
    # ---------------------------------------------------------------------------------------
    # The buy price will be set at a percentage (of your choosing) under the initial price.
    # You can set the initial price manually or use the current market price by setting the
    # command line argument at index 2 as 'automatic'
    # ---------------------------------------------------------------------------------------

    price_dec_plcs = int(asset_args[3])
    amnt_dec_plcs = int(asset_args[4])
    buy_price_divdr = float(sys.argv[3])

    if sys.argv[2].lower() == 'automatic' or sys.argv[2].lower() == 'one':
        initial_price = float(('{:.' + str(price_dec_plcs) + 'f}').format(float(client.get_product(asset_id).to_dict()['price'])))
    elif sys.argv[2].lower() == 'open':
        initial_price = float(('{:.' + str(price_dec_plcs) + 'f}').format(float(get_current_hour_candle(asset_id)['open'])))
    elif sys.argv[2].lower() == 'high':
        initial_price = float(('{:.' + str(price_dec_plcs) + 'f}').format(float(get_current_hour_candle(asset_id)['high'])))
    elif sys.argv[2].lower() == 'low':
        initial_price = float(('{:.' + str(price_dec_plcs) + 'f}').format(float(get_current_hour_candle(asset_id)['low'])))
    elif isinstance(float(sys.argv[2]), float):
        initial_price = float(sys.argv[2])

    initial_buy_price = float(('{:.' + str(price_dec_plcs) + 'f}').format(initial_price - (initial_price * buy_price_divdr)))
    buy_price = initial_buy_price
    
    # -------------------------------------------------------------------------
    # You can either let the sell price multiplier automatically be set to be 
    # the same percentage as your buy price divider, or you can manually set 
    # it to something else
    # -------------------------------------------------------------------------

    if sys.argv[4].lower() == 'automatic':
        sell_price_mltplr = float(f'1{sys.argv[3][1:]}')
    elif isinstance(float(sys.argv[4]), float):
        sell_price_mltplr = float(sys.argv[4])

    sell_price = initial_price # float(('{:.' + str(price_dec_plcs) + 'f}').format(buy_price * (sell_price_mltplr)))
    falling_buy_price = 0
    coin_wallet = [wallet for wallet in all_accounts if wallet['currency'] == coin][0]

    if sys.argv[5] == 'one':
        investment_amount = buy_price
    else:
        investment_amount = float(sys.argv[5])

    accuracy = float(asset_args[9])
    coin_amount = float(('{:.' + str(amnt_dec_plcs) + 'f}').format(investment_amount / buy_price))
    remainder = 0.00
    maker_fee = 0.0025
    fee = 0.004
    # initial_min_currency_bal = 0.0
    size = 0.0

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
    buy_order_type = sys.argv[6].upper()
    delay = float(sys.argv[7])
    # buy_order_wait_count = 0
    # sell_order_wait_count = 0
    count = 0
    # fee = 0.0025
    last_buy_ordr = {}
    last_sell_ordr = {}
    # buy_order_filled = False
    # sell_order_filled = False
    # loop_order = {}

    prefill_buy_order_list = []
    prefill_sell_order_list = []
    filled_buy_order_list = []

    portfolios = client.get_portfolios().to_dict()['portfolios']

    portfolio = client.get_portfolio_breakdown(portfolio_uuid=portfolios[0]['uuid']).to_dict()

    initial_portfolio_balance = float('{:.2f}'.format(float(portfolio['breakdown']['portfolio_balances']['total_balance']['value'])))

    dynamic_portfolio_balance = initial_portfolio_balance
    
    # dynamic_portfolio_balance = float('{:.2f}'.format(float(portfolio['breakdown']['portfolio_balances']['total_balance']['value'])))

    available_balance = float(client.get_account(account_uuid=usd_wallet['uuid']).to_dict()['account']['available_balance']['value'])

    cumulative_balance = dynamic_portfolio_balance

    if available_balance >= investment_amount:
        limit_buy_order = buy(buy_price, buy_order_type, investment_amount, price_dec_plcs, amnt_dec_plcs, coin, asset_id, message='opening buy')
        prefill_buy_order_list.append(limit_buy_order)
    
    while True:

        loop_portfolio = client.get_portfolio_breakdown(portfolio_uuid=portfolios[0]['uuid']).to_dict()
        loop_portfolio_balance = float('{:.2f}'.format(float(loop_portfolio['breakdown']['portfolio_balances']['total_balance']['value'])))
        loop_profit = 0

        if loop_portfolio_balance > cumulative_balance:
            loop_profit = loop_portfolio_balance - cumulative_balance
            cumulative_balance += loop_profit

        if len(prefill_buy_order_list) >= 1:

            for idx, order in enumerate(prefill_buy_order_list):
                filled = False
                order_data = check_if_order_filled(order)
                status = order_data[0]
                
                while not filled:
                    if status:
                        
                        filled = True
                        filled_buy_order_list.append(order_data[1])

                    elif status == None:
                        
                        print('Order cancelled!')
                        prefill_buy_order_list.pop(idx)
                        break
                        
                    else:
                        
                        price = float(client.get_product(asset_id).to_dict()['price'])

                        if price > sell_price:
                            break

                        if delay == 1:
                                print(f'\rBuy order not yet filled. Checking again in 1 second.')
                        else:
                                print(f'\rBuy order not yet filled. Checking again in {str(delay)} seconds.')

                        time.sleep(delay)

                        order_info = check_if_order_filled(order)

                        status = order_info[0]
                        if status:
                            filled = True
                
                if filled:
                    # ----------------------------------------------------------------------------------------------------------
                    # This block of code will always sell for a profit based on what the price was when the buy order was made.
                    # ----------------------------------------------------------------------------------------------------------

                    print(f"{coin} limit buy order {idx + 1} in buy orders list filled!")

                    size = float(order['order_configuration']['limit_limit_gtc']['base_size'])

                    order_price = float(order['order_configuration']['limit_limit_gtc']['limit_price'])

                    order_sell_price = float(('{:.' + str(price_dec_plcs) + 'f}').format(order_price * sell_price_mltplr))

                    limit_sell_order = sell(order_sell_price, size, coin, asset_id)

                    prefill_sell_order_list.append(limit_sell_order)

                    prefill_buy_order_list.pop(idx)

        if len(prefill_sell_order_list) >= 1:

            if cumulative_balance >= (dynamic_portfolio_balance * 1.20):

                dynamic_portfolio_balance = cumulative_balance

                sell_orders_to_cancel_list = []
                market_sell_size = 0

                for order in prefill_sell_order_list:
                    sell_orders_to_cancel_list.append(order['success_response']['order_id'])
                    market_sell_size += float(order['order_configuration']['limit_limit_gtc']['base_size'])

                if len(sell_orders_to_cancel_list) > 0:
                    client.cancel_orders(order_ids=sell_orders_to_cancel_list)
                    
                    if coin_wallet['uuid'] not in [account['uuid'] for account in get_all_accounts()]:

                        if coin_wallet['currency'] in limit_only_market_assets:
                            best_ask_float = float(client.get_best_bid_ask(product_ids=[asset_id]).to_dict()['pricebooks'][0]['asks'][0]['price'])
                            best_ask = ('{:.' + str(amnt_dec_plcs) + 'f}').format(best_ask_float)

                            print("---------------------------")
                            print(f"Selling {coin}!")
                            print(f"Amount selling: {str(market_sell_size)}")
                            print("---------------------------")

                            last_sell_ordr = client.limit_order_gtc_sell(client_order_id=str(generate_client_order_id()), product_id=asset_id, base_size=str(market_sell_size), limit_price=best_ask)

                            with open(f'[{dt.now().strftime("%b_%d_%Y")}]last_sell_order.json', 'w') as file:

                                json.dump(last_sell_ordr.to_dict(), file, indent=6)
                        else:

                            print("---------------------------")
                            print(f"Selling {coin}!")
                            print(f"Amount selling: {str(market_sell_size)}")
                            print("---------------------------")

                            last_sell_ordr = client.market_order_sell(client_order_id=str(generate_client_order_id()), product_id=asset_id, base_size=str(market_sell_size))

                            with open(f'[{dt.now().strftime("%b_%d_%Y")}]last_sell_order.json', 'w') as file:

                                json.dump(last_sell_ordr.to_dict(), file, indent=6)
                    else:
                        asset_available_balance_float = float(client.get_account(account_uuid=coin_wallet['uuid']).to_dict()['account']['available_balance']['value'])
                        asset_available_balance = ('{:.' + str(amnt_dec_plcs) + 'f}').format(asset_available_balance_float)

                        if coin_wallet['currency'] in limit_only_market_assets:
                            best_ask_float = float(client.get_best_bid_ask(product_ids=[asset_id]).to_dict()['pricebooks'][0]['asks'][0]['price'])
                            best_ask = ('{:.' + str(amnt_dec_plcs) + 'f}').format(best_ask_float)

                            print("---------------------------")
                            print(f"Selling {coin}!")
                            print(f"Amount selling: {asset_available_balance}")
                            print("---------------------------")

                            last_sell_ordr = client.limit_order_gtc_sell(client_order_id=str(generate_client_order_id()), product_id=asset_id, base_size=asset_available_balance, limit_price=best_ask)

                            with open(f'[{dt.now().strftime("%b_%d_%Y")}]last_sell_order.json', 'w') as file:

                                json.dump(last_sell_ordr.to_dict(), file, indent=6)
                        else:

                            print("---------------------------")
                            print(f"Selling {coin}!")
                            print(f"Amount selling: {asset_available_balance}")
                            print("---------------------------")

                            last_sell_ordr = client.market_order_sell(client_order_id=str(generate_client_order_id()), product_id=asset_id, base_size=asset_available_balance)

                            with open(f'[{dt.now().strftime("%b_%d_%Y")}]last_sell_order.json', 'w') as file:

                                json.dump(last_sell_ordr.to_dict(), file, indent=6)

            for idx, order in enumerate(prefill_sell_order_list):
                order_info = check_if_order_filled(order)
                filled = order_info[0]

                if filled:
                    print(f"{coin} limit sell order {idx + 1} in sell orders list filled!")
                    prefill_sell_order_list.pop(idx)
                elif filled == None:
                    print('Order cancelled!')
                    prefill_sell_order_list.pop(idx)
                else:
                    if delay == 1:
                        print(f'\rSell order not yet filled. Checking again in 1 second.')
                    else:
                        print(f'\rSell order not yet filled. Checking again in {str(delay)} seconds.')


        price = float(client.get_product(asset_id).to_dict()['price'])

        if price <= buy_price and count > 0:

            wallet = client.get_account(account_uuid=usd_wallet['uuid']).to_dict()['account']

            available_balance = float(wallet['available_balance']['value'])

            if available_balance >= investment_amount:

                if available_balance <= dynamic_portfolio_balance * 0.75 and available_balance > dynamic_portfolio_balance * 0.5:

                    # if available_balance > initial_portfolio_balance:

                    #     delay = float(sys.argv[7])

                    # else:

                    #     delay = 150

                    buy_price_divdr = 0.075

                    sell_price_mltplr = 1.05

                elif available_balance <= dynamic_portfolio_balance * 0.5:

                    # if available_balance > initial_portfolio_balance:

                    #     delay = float(sys.argv[7])
                        
                    # else:

                    #     delay = 300

                    buy_price_divdr = 0.1
                    
                    sell_price_mltplr = 1.075
                
                else:

                    # delay = float(sys.argv[7])

                    buy_price_divdr = float(sys.argv[3])

                    if sys.argv[4].lower() == 'automatic':
                        sell_price_mltplr = float(f'1{sys.argv[3][1:]}')
                    elif isinstance(float(sys.argv[4]), float):
                        sell_price_mltplr = float(sys.argv[4])
               
                # -------------------------------------------------------------------
                # Adjust the buy and sell prices in correspondence with the market
                # -------------------------------------------------------------------

                if price < buy_price:

                    if price < initial_buy_price and falling_buy_price == 0:
                        falling_buy_price = float(('{:.' + str(price_dec_plcs) + 'f}').format(price - (price * buy_price_divdr)))
                        buy_price = falling_buy_price

                    elif price < initial_buy_price and falling_buy_price > 0 and price > falling_buy_price:
                        buy_price = falling_buy_price

                    elif price <= falling_buy_price:
                        falling_buy_price = float(('{:.' + str(price_dec_plcs) + 'f}').format(price - (price * buy_price_divdr)))
                        buy_price = falling_buy_price

                    else:
                        buy_price = float(('{:.' + str(price_dec_plcs) + 'f}').format(price))
                        sell_price = float(('{:.' + str(price_dec_plcs) + 'f}').format(buy_price * (sell_price_mltplr)))
                    # buy_price = float(('{:.' + str(price_dec_plcs) + 'f}').format(price))
                    # sell_price = float(('{:.' + str(price_dec_plcs) + 'f}').format(buy_price * (sell_price_mltplr)))

                best_bid = float(client.get_best_bid_ask(product_ids=[asset_id]).to_dict()['pricebooks'][0]['bids'][0]['price'])

                if sys.argv[5] == 'one':
                    investment_amount = best_bid

                limit_buy_order = buy(best_bid, buy_order_type, investment_amount, price_dec_plcs, amnt_dec_plcs, coin, asset_id)
                prefill_buy_order_list.insert(0, limit_buy_order)

                print(cur + ' Available: ' + ('{:.2f}').format(available_balance))
                print(f"Buy price: ${str(buy_price)}")
                print(f'Sell price: ${str(sell_price)}')
                if delay == 1:
                   print(f'Checking again in {str(delay)} second...')
                else:
                   print(f'Checking again in {str(delay)} seconds...')
                print('---------------------------------------------\n')
 
            else:
                print('---------------------------------------------\n')
                print('Your account balance is below the minumum required to trade.')
                print(f'Minimum amount required: ${"{:.2f}".format(investment_amount)}')
                print(f"Current available balance: ${'{:.4f}'.format(available_balance)}")
                
                print(f"Buy price: ${str(buy_price)}")
                print(f'Sell price: ${str(sell_price)}')

                if delay == 1:
                   print(f'Checking again in {str(delay)} second...')
                else:
                   print(f'Checking again in {str(delay)} seconds...')
                print('---------------------------------------------\n')

        elif price >= sell_price:

            wallet = client.get_account(account_uuid=usd_wallet['uuid']).to_dict()['account']

            available_balance = float(wallet['available_balance']['value'])

            if available_balance >= investment_amount:

                if available_balance <= dynamic_portfolio_balance * 0.75 and available_balance > dynamic_portfolio_balance * 0.5:

                    # if available_balance > initial_portfolio_balance:

                    #     delay = float(sys.argv[7])
                        
                    # else:

                    #     delay = 150

                    buy_price_divdr = 0.075

                    sell_price_mltplr = 1.05

                elif available_balance <= dynamic_portfolio_balance * 0.5:

                    # if available_balance > initial_portfolio_balance:

                    #     delay = float(sys.argv[7])
                        
                    # else:

                    #     delay = 300

                    buy_price_divdr = 0.1
                    
                    sell_price_mltplr = 1.075
                
                else:

                    # delay = float(sys.argv[7])

                    buy_price_divdr = float(sys.argv[3])

                    if sys.argv[4].lower() == 'automatic':
                        sell_price_mltplr = float(f'1{sys.argv[3][1:]}')
                    elif isinstance(float(sys.argv[4]), float):
                        sell_price_mltplr = float(sys.argv[4])

                # -------------------------------------------------------------------
                # Adjust the buy and sell prices in correspondence with the market
                # -------------------------------------------------------------------

                # multiplier = float(f'1{float(sys.argv[3][1:]) * 2}')

                if price > sell_price: # (sell_price * multiplier):
                    sell_price = float(('{:.' + str(price_dec_plcs) + 'f}').format(price * sell_price_mltplr)) 
                    buy_price = float(('{:.' + str(price_dec_plcs) + 'f}').format(sell_price - (sell_price * buy_price_divdr)))

                if  len(prefill_buy_order_list) > 0:

                    buy_orders_to_cancel_list = []
                    current_buy_price = buy_price

                    for idx, order in enumerate(prefill_buy_order_list):
                        order_price = float(order['order_configuration']['limit_limit_gtc']['limit_price'])
                        if order_price < current_buy_price:
                            buy_orders_to_cancel_list.append(order['success_response']['order_id'])
                    
                    if len(buy_orders_to_cancel_list) > 0:
                        print('Cancelling all buy orders under current buy price!')
                        client.cancel_orders(order_ids=buy_orders_to_cancel_list)

                if sys.argv[5] == 'one':
                    investment_amount = buy_price

                limit_buy_order = buy(buy_price, buy_order_type, investment_amount, price_dec_plcs, amnt_dec_plcs, coin, asset_id, message='sell')
                prefill_buy_order_list.insert(0, limit_buy_order)


                print(f"Buy price: ${str(buy_price)}")
                print(f'Sell price: ${str(sell_price)}')
                if delay == 1:
                    print(f'Checking again in {str(delay)} second...')
                else:
                    print(f'Checking again in {str(delay)} seconds...')
                print('---------------------------------------------\n')
                
            else:
                print('---------------------------------------------\n')
                print('Your account balance is below the minumum required to trade.')
                print(f'Minimum amount required: ${"{:.2f}".format(investment_amount)}')
                print(f"Current available balance: ${'{:.4f}'.format(available_balance)}")
                print(f"Buy price: ${str(buy_price)}")
                print(f'Sell price: ${str(sell_price)}')

                if delay == 1:
                    print(f'Checking again in {str(delay)} second...')
                else:
                    print(f'Checking again in {str(delay)} seconds...')
                    print('---------------------------------------------\n')
                
                
        else:
            print('\nThe market is trending upwards but\n'
                  'you either haven\'t bought in yet \n'
                 f"(buy price: ${str(buy_price)}) or you\'ve bought\n"
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