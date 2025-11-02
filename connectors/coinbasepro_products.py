from coinbase.rest import RESTClient
from coinbase.websocket import WSClient, WebsocketResponse
# from coinbase.websocket import WSUserClient
from datetime import datetime as dt
from env.api_key import *
import math
import json
import uuid

creds = load_api_credentials()
# limit_buy_order_id = ''
# limit_sell_order_id = ''
# market_buy_order_id = ''
# market_sell_order_id = ''
# limit_buy_order_filled = False
# limit_sell_order_filled = False
# market_buy_order_filled = False
# market_sell_order_filled = False
flld_buy_ordr = {}
flld_sell_ordr = {}

def generate_client_order_id():
    return uuid.uuid4()

client = RESTClient(api_key=creds[0], api_secret=creds[1])
# client = RESTClient(api_key=creds[0], api_secret=creds[1], verbose=True)
# ws_user_client = WSUserClient(api_key=creds[0], api_secret=creds[1], on_message=on_message, verbose=True)

def check_if_order_filled(order):
    global flld_buy_ordr
    global flld_sell_ordr
    side = order['success_response']['side']

    order_data = client.get_order(order['success_response']['order_id']).to_dict()['order']
    
    if order_data['side'] == 'BUY' and order_data['status'] == 'FILLED':

        flld_buy_ordr = order_data

        with open(f'[{dt.now().strftime("%b_%d_%Y")}]filled_buy_order.json', 'w') as file:
            json.dump(flld_buy_ordr, file, indent=6)

        return True
    elif order_data['side'] == 'SELL' and order_data['status'] == 'FILLED':
        flld_sell_ordr = order_data

        with open(f'[{dt.now().strftime("%b_%d_%Y")}]filled_sell_order.json', 'w') as file:
            json.dump(flld_sell_ordr, file, indent=6)

        return True
    elif order_data['status'] == 'CANCELLED':

        return None 
    else:
        return False
            

def buy(buy_price, buy_order_type, set_usd_accnt_bal, price_dec_plcs, amnt_dec_plcs, coin, asset_id):

    spcl_assts = ['SHIB', 'BONK', 'VTHO', 'SPELL', 'SHPING']

    if buy_order_type == 'ONE':
        # For Limit Buy Orders That Don't Allow Decimal Sizes
        fiat_cur = '{:.2f}'.format(math.floor(set_usd_accnt_bal / buy_price))
    elif buy_order_type == 'TWO':
        # For Limit Buy Taker Orders That Don't Allow Decimal Sizes                    
        coin_amnt = '{:.2f}'.format(math.floor(set_usd_accnt_bal / buy_price))
        fiat_cur = coin_amnt
    elif buy_order_type == 'THREE':
        # For Limit Buy Orders That Allow Decimal Sizes
        fiat_cur = ('{:.' + str(amnt_dec_plcs) + 'f}').format(set_usd_accnt_bal / buy_price)
    elif buy_order_type == 'FOUR':
        # For Limit Buy Taker Orders That Allow Decimal Sizes                    
        coin_amnt = ('{:.' + str(amnt_dec_plcs) + 'f}').format(set_usd_accnt_bal / buy_price)
        fiat_cur = coin_amnt


    
    print('Buying ' + coin + '!')
    print(f'Buy price: ${str(buy_price)}')
    
    # Limit Buy Order (Max)
    if coin in spcl_assts:
        last_buy_ordr = client.limit_order_gtc_buy(client_order_id=str(generate_client_order_id()),product_id=asset_id,base_size=fiat_cur,limit_price=('{:.' + str(price_dec_plcs) + 'f}').format(buy_price))

        with open(f'[{dt.now().strftime("%b_%d_%Y")}]last_buy_order.json', 'w') as file:

            json.dump(last_buy_ordr.to_dict(), file, indent=6)

    else:
        last_buy_ordr = client.limit_order_gtc_buy(client_order_id=str(generate_client_order_id()),product_id=asset_id,base_size=fiat_cur,limit_price=str(buy_price))

        with open(f'[{dt.now().strftime("%b_%d_%Y")}]last_buy_order.json', 'w') as file:

            json.dump(last_buy_ordr.to_dict(), file, indent=6)

    return last_buy_ordr


def sell(sell_price, amount, coin, asset_id):

    print(f"Selling {coin}!")
    print(f'Sell price: ${str(sell_price)}')

    last_sell_ordr = client.limit_order_gtc_sell(client_order_id=str(generate_client_order_id()), product_id=asset_id, base_size=str(amount), limit_price=str(sell_price))

    with open(f'[{dt.now().strftime("%b_%d_%Y")}]last_sell_order.json', 'w') as file:

        json.dump(last_sell_ordr.to_dict(), file, indent=6)


    return last_sell_ordr
            

def get_assets_args_setup_list(filename):
    assets_args_setup_list = []

    with open(filename, 'r') as file:
        for asset_args in file.readlines():
            assets_args_setup_list.append(asset_args.split())

    return assets_args_setup_list

def get_all_assets(filename):
    read_all_accounts_from_json = []
    with open(filename, 'r') as file:
        read_all_accounts_from_json = json.load(file)

    return read_all_accounts_from_json

def get_asset_args_setup(lst, sys_argv):
    asset_args_setup = []
    for args in lst:
        if sys_argv == args[6] or sys_argv == args[7]:
            asset_args_setup = args

    return asset_args_setup