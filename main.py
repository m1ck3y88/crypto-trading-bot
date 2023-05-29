# import tkinter as tk

from connectors.coinbasepro_products import *
import time
import math

# logger = logging.getLogger()
#
# logger.setLevel(logging.INFO)
#
# stream_handler = logging.StreamHandler()
# formatter = logging.Formatter('%(asctime)s %(levelname)s :: %(message)s')
# stream_handler.setFormatter(formatter)
# stream_handler.setLevel(logging.INFO)
#
# file_handler = logging.FileHandler('info.log')
# file_handler.setFormatter(formatter)
# file_handler.setLevel(logging.DEBUG)
#
# logger.addHandler(stream_handler)
# logger.addHandler(file_handler)

if __name__ == '__main__':

    # Live Account Limit Buy/Limit Sell Algorithm
    cur = 'USD'
    buy_price = float(input("Please enter the buy price: "))
    sell_price = float(input("Please enter the sell price: "))
    coin = input("Please enter the coin abbreviation for the coin\n"
                 "you are investing in\n"
                 "Example: BTC\n").upper()
    asset_id = input("Please enter the asset you want to invest in\n"
                     "using the following format: asset-currency\n"
                     "Example: BTC-USD\n").upper()
    min_currency_bal = float(input("Please enter minimum balance of your\n"
                                   "native currency you choose to have in order to trade: "))
    min_asset_bal = float(input("Please enter minimum balance of your asset (cryptocurrency)\n"
                                "you choose to have in order to trade: "))
    # lmtbuy_asst_amnt = float(input("Please enter the amount of the asset\n"
    #                                 "you want to purchase: "))
    delay = int(input("Please enter the number of seconds you choose to wait before checking\n"
                      "to buy/sell again: "))
    count = 0

    while True:
        price = float(auth_client.get_product_ticker(product_id=asset_id)['price'])
        if price <= buy_price:
            # buy_price = price
            for wallet in get_live_accounts():
                if wallet['currency'] == cur and float(wallet['balance']) >= min_currency_bal:
                    print('Buying ' + coin + '!')
                    # For Cryptocurrency Worth Less Than a Dollar
                    fiat_cur = '{:.2f}'.format(int((float(wallet['balance']) / price) -
                                               ((float(wallet['balance']) / price) * 0.004)))
                    # For Cryptocurrency Worth More Than a Dollar
                    # fiat_cur = '{:.3f}'.format((float(wallet['balance']) / price) -
                    #                                ((float(wallet['balance']) / price) * 0.004))
                    # For Coins That Don't Allow Decimal Purchases (i.e. SHIBA)
                    # fiat_cur = str(int((float(wallet['balance']) / price) -
                    #                                ((float(wallet['balance']) / price) * 0.004)))
                    # For Market Buy Orders
                    # fiat_cur = '{:.2f}'.format(math.floor(float(wallet['balance'])))
                    # print(fiat_cur)
                    print(cur + ' Available: ' + '{:.2f}'.format(float(wallet['balance'])))
                    # Limit Buy Order (Max)
                    auth_client.place_limit_order(product_id=asset_id, side='buy', price=str(price),
                                                  size=fiat_cur)
                    # Limit Buy Order (Choose Amount of Cryptocurrency You Want to Buy)
                    # auth_client.place_limit_order(product_id=asset_id, side='buy', price=str(price),
                    #                               size=str(lmtbuy_asst_amnt))
                    # Market Buy Order
                    # auth_client.place_market_order(product_id=asset_id, side='buy', funds=fiat_cur)
                    if delay == 1:
                        print(f'Checking again in {str(delay)} second...')
                    else:
                        print(f'Checking again in {str(delay)} seconds...')
                    print('---------------------------------------------\n')
                else:
                    if wallet['currency'] == coin and float(wallet['balance']) >= min_asset_bal:
                        if count == 0:
                            print('Your\'re already invested in ' + coin + '!')
                            print(coin + ' Available: ' + '{:.2f}'.format(float(wallet['balance'])))
                            if delay == 1:
                                print(f'Checking again in {str(delay)} second...')
                            else:
                                print(f'Checking again in {str(delay)} seconds...')
                            print('---------------------------------------------\n')
                            count += 1
                        else:
                            print('The market is trending downwards')
                            if delay == 1:
                                print(f'Checking again in {str(delay)} second...')
                            else:
                                print(f'Checking again in {str(delay)} seconds...')
                            print('---------------------------------------------\n')

        elif price >= sell_price:
            for asset in get_live_accounts():
                if asset['currency'] == coin and float(asset['balance']) >= min_asset_bal:
                    print('You made a profit! Selling ' + coin + '!')
                    coin_cur = asset['balance']
                    print(coin + ' Available: ' + coin_cur)
                    # Limit Sell Order (Choose Amount of Cryptocurrency You Want to Buy)
                    # auth_client.place_limit_order(product_id=asset_id, side='sell', price=str(price),
                    #                               size=str(lmttbuy_asst_amnt))
                    # Limit Sell Order (Max)
                    auth_client.place_limit_order(product_id=asset_id, side='sell', price=str(price), size=coin_cur)
                    # Market Sell Order
                    # auth_client.place_market_order(product_id=asset_id, side='sell', funds=coin_cur)
                else:
                    if asset['currency'] == cur and float(asset['balance']) >= min_currency_bal:
                        print('You\'ve already made a profit\n'
                              'and are waiting to buy back in')
                        print(cur + ' Available: ' + '{:.2f}'.format(float(asset['balance'])))
                        if delay == 1:
                            print(f'Checking again in {str(delay)} second...')
                        else:
                            print(f'Checking again in {str(delay)} seconds...')
                        print('---------------------------------------------\n')

        else:
            print('\nThe market is trending upwards but\n'
                  'you either haven\'t bought in yet or you\'ve\n'
                  'bought in and the market price hasn\'t reached\n'
                  'your target sell price yet')
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
    #             if wallet['currency'] == sb_cur and float(wallet['balance']) >= sb_min_currency_bal:
    #                 print('Buying ' + sb_coin + '!')
    #                 # For Cryptocurrency Worth More Than a Dollar
    #                 fiat_cur = '{:.8f}'.format((float(wallet['balance']) / price) -
    #                                            ((float(wallet['balance']) / price) * 0.006))
    #                 print(wallet)
    #                 # sb_lmtbuy_asst_amnt = '{:.2f}'.format(math.floor(float(fiat_cur)/sb_buy_price))
    #                 # print('Currency balance converted to cryptocurrency: ' + sb_lmtbuy_asst_amnt)
    #                 print(sb_cur + ' Available: ' + '{:.2f}'.format(float(wallet['balance'])))
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
    #                 if wallet['currency'] == sb_coin and float(wallet['balance']) >= sb_min_asset_bal:
    #                     if sb_count == 0:
    #                         print('Your\'re already invested in ' + sb_coin + '!')
    #                         print(sb_coin + ' Available: ' + '{:.2f}'.format(float(wallet['balance'])))
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
    #             if asset['currency'] == sb_coin and float(asset['balance']) >= sb_min_asset_bal:
    #                 print('You made a profit! Selling ' + sb_coin + '!')
    #                 # '{:.2f}'.format(math.floor(float(asset['balance'])))
    #                 # '{:.2f}'.format(float(asset['balance']))
    #                 coin_cur = asset['balance']
    #                 print(sb_coin + ' Available: ' + coin_cur)
    #                 # auth_sandbox_client.place_limit_order(product_id=sb_asset_id, side='sell', price=str(sb_sell_price),
    #                 #                               size=str(sb_lmtbuy_asst_amnt))
    #                 auth_sandbox_client.place_limit_order(product_id=sb_asset_id, side='sell', price=str(price), size=coin_cur)
    #                 # auth_sandbox_client.place_market_order(product_id=sb_asset_id, side='sell', funds=coin_cur)
    #             else:
    #                 if asset['currency'] == sb_cur and float(asset['balance']) >= sb_min_currency_bal:
    #                     print('You\'ve already made a profit\n'
    #                           'and are waiting to buy back in')
    #                     print(sb_cur + ' Available: ' + '{:.2f}'.format(float(asset['balance'])))
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

    # root = tk.Tk()
    # root.configure(bg='gray12')
    #
    # i = 0
    # j = 0
    #
    # calibri_font = ("Calibri", 11, "normal")
    #
    # for product in sandbox_products:
    #     label_widget = tk.Label(root, text=product, bg='gray12', fg='SteelBlue1', width=13)
    #     label_widget.grid(row=i, column=j, sticky='ew')
    #
    #     if i == 4:
    #         j += 1
    #         i = 0
    #     else:
    #         i += 1
    #
    # root.mainloop()