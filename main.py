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

    # Live Account Algorithm
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
    delay = int(input("Please enter the number of seconds you choose to wait before checking\n"
                      "to buy/sell again: "))
    count = 0
    # filled_buy_price = float(input("Set this to a high number that you know the asset\n"
    #                                "you're investing in most likely won't reach"))

    while True:
        price = float(auth_client.get_product_ticker(product_id=asset_id)['price'])
        if price <= buy_price:
            for wallet in get_live_accounts():
                if wallet['currency'] == cur and float(wallet['balance']) >= min_currency_bal:
                    print('Buying ' + coin + '!')
                    fiat_cur = '{:.2f}'.format(math.floor(float(wallet['balance'])))
                    print(cur + ' Available: ' + '{:.2f}'.format(float(wallet['balance'])))
                    auth_client.place_market_order(product_id=asset_id, side='buy', funds=fiat_cur)
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

        elif price >= sell_price or price >= buy_price * 20:
            for asset in get_live_accounts():
                if asset['currency'] == coin and float(asset['balance']) >= min_asset_bal:
                    print('You made a profit! Selling ' + coin + '!')
                    # '{:.2f}'.format(math.floor(float(asset['balance'])))
                    # '{:.2f}'.format(float(asset['balance']))
                    coin_cur = asset['balance']
                    print(coin + ' Available: ' + coin_cur)
                    auth_client.place_market_order(product_id=asset_id, side='sell', size=coin_cur)
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
    #
    # while True:
    #     sb_price = float(auth_sandbox_client.get_product_ticker(product_id=sb_asset_id)['price'])
    #     if sb_price <= sb_buy_price:
    #         for sb_wallet in get_sandbox_accounts():
    #             if sb_wallet['currency'] == sb_cur and float(sb_wallet['balance']) >= 10:
    #                 print('Buying ' + sb_coin + '!')
    #                 sb_fiat_cur = '{:.2f}'.format(math.floor(float(sb_wallet['balance'])))
    #                 print(sb_cur + ' Available: ' + sb_fiat_cur)
    #                 auth_sandbox_client.place_market_order(product_id=sb_asset_id, side='buy', funds=sb_fiat_cur)
    #     elif sb_price >= sb_sell_price or sb_price <= sb_buy_price * 1.01:
    #         for sb_asset in get_sandbox_accounts():
    #             if sb_asset['currency'] == sb_coin and float(sb_asset['balance']) >= 5:
    #                 print('Selling ' + sb_coin + '!')
    #                 sb_coin_cur = sb_asset['balance']
    #                 print(sb_coin + ' Available: ' + sb_coin_cur)
    #                 auth_sandbox_client.place_market_order(product_id=sb_asset_id, side='sell', size=sb_coin_cur)
    #
    #     else:
    #         print('Nothing yet...')
    #     time.sleep(5)

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
