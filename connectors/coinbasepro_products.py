from coinbase.rest import RESTClient 
from coinbase.websocket import WSClient, WebsocketResponse 
# from coinbase.websocket import WSUserClient
from datetime import datetime as dt, timezone as tz, timedelta
from env.api_key import *
from pathlib import Path
from enum import Enum
import pandas as pd
import math
import json
import uuid
import time
import os
import ta 

class Granularity(Enum):
    UNKNOWN = 'UNKNOWN_GRANULARITY'
    ONE_MINUTE = 'ONE_MINUTE'
    FIVE_MINUTES = 'FIVE_MINUTE'
    FIFTEEN_MINUTES = 'FIFTEEN_MINUTE'
    THIRTY_MINUTES = 'THIRTY_MINUTE'
    ONE_HOUR = 'ONE_HOUR'
    TWO_HOUR = 'TWO_HOUR'
    FOUR_HOUR = 'FOUR_HOUR'
    SIX_HOUR = 'SIX_HOUR'
    ONE_DAY = 'ONE_DAY'


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
ws_data = []

def generate_client_order_id():
    return uuid.uuid4()

client = RESTClient(api_key=creds[0], api_secret=creds[1])
# client = RESTClient(api_key=creds[0], api_secret=creds[1], verbose=True)
# ws_client = WSClient(api_key=creds[0], api_secret=creds[1], on_message=on_message)
# ws_user_client = WSUserClient(api_key=creds[0], api_secret=creds[1], on_message=on_message, verbose=True)


def check_if_order_filled(order):
    global flld_buy_ordr
    global flld_sell_ordr

    order_data = client.get_order(order['success_response']['order_id']).to_dict()['order']
    
    if order_data['side'] == 'BUY' and order_data['status'] == 'FILLED':

        flld_buy_ordr = order_data

        filename = f'[{dt.now().strftime("%b_%d_%Y")}]filled_buy_orders.json'

        if not os.path.exists(filename):

            Path(filename).touch()

            with open(filename, 'w') as file:
            
                json.dump(flld_buy_ordr, file, indent=6)

        else:

            json_file_data_list = []

            with open(filename, 'r') as file:
            
                json_file_data = json.load(file)

                if isinstance(json_file_data, dict):
                    
                    json_file_data_list.append(json_file_data)
                    
                elif isinstance(json_file_data, list):
                    
                    for obj in json_file_data:
    
                        json_file_data_list.append(obj)

            json_file_data_list.append(flld_buy_ordr)

            with open(filename, 'w') as file:

                json.dump(json_file_data_list, file, indent=6)

        return [True, flld_buy_ordr]
    
    elif order_data['side'] == 'SELL' and order_data['status'] == 'FILLED':

        flld_sell_ordr = order_data

        filename = f'[{dt.now().strftime("%b_%d_%Y")}]filled_sell_orders.json'

        if not os.path.exists(filename):

            Path(filename).touch()

            with open(filename, 'w') as file:
            
                json.dump(flld_sell_ordr, file, indent=6)

        else:

            json_file_data_list = []

            with open(filename, 'r') as file:
            
                json_file_data = json.load(file)

                if isinstance(json_file_data, dict):
                    
                    json_file_data_list.append(json_file_data)
                    
                elif isinstance(json_file_data, list):
                    
                    for obj in json_file_data:
    
                        json_file_data_list.append(obj)

            json_file_data_list.append(flld_sell_ordr)

            with open(filename, 'w') as file:

                json.dump(json_file_data_list, file, indent=6)

        return [True, flld_sell_ordr]
    
    elif order_data['status'] == 'CANCELLED':

        filename = f'[{dt.now().strftime("%b_%d_%Y")}]cancelled_orders.json'

        if not os.path.exists(filename):

            Path(filename).touch()

            with open(filename, 'w') as file:
            
                json.dump(order_data, file, indent=6)

        else:

            json_file_data_list = []

            with open(filename, 'r') as file:
            
                json_file_data = json.load(file)

                if isinstance(json_file_data, dict):
                    
                    json_file_data_list.append(json_file_data)
                    
                elif isinstance(json_file_data, list):
                    
                    for obj in json_file_data:
    
                        json_file_data_list.append(obj)

            json_file_data_list.append(order_data)

            with open(filename, 'w') as file:

                json.dump(json_file_data_list, file, indent=6)

        return [None, order_data] 
    
    else:

        filename = f'[{dt.now().strftime("%b_%d_%Y")}]open_orders.json'

        if not os.path.exists(filename):

            Path(filename).touch()

            with open(filename, 'w') as file:
            
                json.dump(order_data, file, indent=6)

        else:

            open_orders = []

            with open(filename, 'r') as file:

                json_file_data = json.load(file)

                if isinstance(json_file_data, dict):

                    open_orders.append(json_file_data)

                elif isinstance(json_file_data, list):

                    for obj in json_file_data:
                        
                        if not obj['order_id'] == order_data['order_id']:
                            open_orders.append(obj)

                for idx, obj in enumerate(open_orders):

                    file_data = client.get_order(obj['order_id']).to_dict()['order']

                    if not file_data['status'] == 'OPEN':
                        open_orders.pop(idx)

            open_orders.append(order_data)

            with open(filename, 'w') as file:

                json.dump(open_orders, file, indent=6)

        return [False, order_data]
            

def buy(buy_price, buy_order_type, set_usd_accnt_bal, price_dec_plcs, amnt_dec_plcs, coin, asset_id, message='buy'):

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


    
    if message == 'buy':
        print('Buying ' + coin + ' at best bid!')
        print(f'Best bid: ${str(buy_price)}')
    else:
        print('Buying ' + coin + '!')
        print(f'Order price: ${str(buy_price)}')
    
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
            

def get_accounts_data(cursor=None):
    return client.get_accounts(limit=250, cursor=cursor).to_dict()

def get_all_accounts():
    all_accounts = []
    hasnext = True
    data = get_accounts_data()

    for account in data['accounts']:
            all_accounts.append(account)
        
    while hasnext:
        new_data = get_accounts_data(data['cursor'])

        for paginated_account in new_data['accounts']:
            all_accounts.append(paginated_account)

        data = new_data

        if not new_data['has_next']:
            hasnext = False
        
    return all_accounts

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

def get_unix_utc_time_at_start_of_day():
    """
    Returns the Unix timestamp (seconds since epoch) for the start of a
    particular day in the UTC timezone.

    Returns:
        int: The Unix timestamp.
    """
    datetime_string_split = dt.now().strftime('%Y %m %d').split()
    year = int(datetime_string_split[0])
    month = int(datetime_string_split[1])
    day = int(datetime_string_split[2])
    
    dt_object = dt(year, month, day, 0, 0, 0)
    return str(int(dt_object.timestamp()))

def get_unix_utc_time_at_start_of_hour():
    """
    Returns the Unix timestamp (seconds since epoch) for the start of a
    particular hour in the UTC timezone.

    Returns:
        int: The Unix timestamp.
    """
    datetime_string_split = dt.now().strftime('%Y %m %d %H').split()
    year = int(datetime_string_split[0])
    month = int(datetime_string_split[1])
    day = int(datetime_string_split[2])
    hour = int(datetime_string_split[3])
    
    dt_object = dt(year, month, day, hour, 0, 0)
    return str(int(dt_object.timestamp()))

def get_current_hour_candle(asset_id):
    start = get_unix_utc_time_at_start_of_hour()
    end = str(int(get_unix_utc_time_at_start_of_hour()) + 3600)
    granularity = Granularity.ONE_HOUR.value

    asset_candle = client.get_candles(asset_id, start, end, granularity).to_dict()['candles'][0]

    asset_candle['start'] = dt.fromtimestamp(int(asset_candle['start'])).strftime('%b %d, %Y %I:%M %p')

    return asset_candle

def get_daily_candles(asset_id, days):
    dt_obj = dt.fromtimestamp(int(get_unix_utc_time_at_start_of_day())) - timedelta(days=days)
    start = str(int(dt_obj.timestamp()))
    end = get_unix_utc_time_at_start_of_day()
    granularity = Granularity.ONE_DAY.value

    asset_candles = client.get_candles(asset_id, start, end, granularity).to_dict()['candles']

    for obj in asset_candles:
        obj['start'] = dt.fromtimestamp(int(obj['start'])).strftime('%b %d, %Y %I:%M %p')

    return asset_candles

def get_hourly_candles(asset_id, hours):
    dt_obj = dt.fromtimestamp(int(get_unix_utc_time_at_start_of_hour())) - timedelta(hours=hours)
    start = str(int(dt_obj.timestamp()))
    end = get_unix_utc_time_at_start_of_hour()
    granularity = Granularity.ONE_HOUR.value

    asset_candles = client.get_candles(asset_id, start, end, granularity).to_dict()['candles']

    for obj in asset_candles:
        obj['start'] = dt.fromtimestamp(int(obj['start'])).strftime('%b %d, %Y %I:%M %p')

    return asset_candles

def get_asset_daily_SMA_20_RSI_14(asset_id, days):
    asset_df = pd.DataFrame(get_daily_candles(asset_id, days))
    asset_df['close'] = pd.to_numeric(asset_df['close'])
    asset_df['SMA_20'] = asset_df['close'].rolling(window=20).mean()
    asset_df['RSI_14'] = ta.momentum.RSIIndicator(asset_df['close'], window=14).rsi()

    # print(asset_df[['close', 'SMA_20', 'RSI_14']].tail())

    return (asset_id, asset_df)

def get_asset_hourly_SMA_20_RSI_14(asset_id, hours):
    asset_df = pd.DataFrame(get_hourly_candles(asset_id, hours))
    asset_df['close'] = pd.to_numeric(asset_df['close'])
    asset_df['SMA_20'] = asset_df['close'].rolling(window=20).mean()
    asset_df['RSI_14'] = ta.momentum.RSIIndicator(asset_df['close'], window=14).rsi()

    # print(asset_df[['close', 'SMA_20', 'RSI_14']].tail())

    return (asset_id, asset_df)

def get_assets_with_daily_RSI_at_or_above_70(days, accounts_list=get_all_assets('all_accounts_[Dec_12_2025].json')):
    assets_RSI_14_at_or_above_70 = []
    all_assets_SMA_20_RSI_14 = []
    
    for idx, account in enumerate(accounts_list):
        try:
            tup = get_asset_daily_SMA_20_RSI_14(f"{account['currency']}-USD", days)
        except Exception as e:
            print('----------------------')
            print('There was an error at index #' + str(idx) + '. Asset: ' + account['currency'] + '-USD')
            print('Error message: ' + str(e))
            print('----------------------')
    
        asset_sma_20_rsi_14_dict = tup[1].tail().iloc[4, [0, 5, 6, 7]].to_dict()

        asset_sma_20_rsi_14_dict['product_id'] = tup[0]
    
        all_assets_SMA_20_RSI_14.append(asset_sma_20_rsi_14_dict)

    for idx, asset in enumerate(all_assets_SMA_20_RSI_14):
        if asset['RSI_14'] >= 70:
            assets_RSI_14_at_or_above_70.append(asset)
        # else:
        #     if idx == 0:
        #         print(f"{asset['product_id']} has an RSI below 70")
        #         print(f"RSI: {str(asset['RSI_14'])}")
        #         print("Checking next asset...")
        #         print()
        #         print('---------------------------')
        #     else:
        #         print()
        #         print(f"{asset['product_id']} has an RSI below 70")
        #         print(f"RSI: {str(asset['RSI_14'])}")
        #         print("Checking next asset...")
        #         print()
        #         print('---------------------------')
    return {"all_assets_SMA_20_and_RSI_14": all_assets_SMA_20_RSI_14, "assets_RSI_14_at_or_above_70": assets_RSI_14_at_or_above_70}

def get_assets_with_hourly_RSI_at_or_above_70(hours, accounts_list=get_all_assets('all_accounts_[Dec_12_2025].json')):
    assets_RSI_14_at_or_above_70 = []
    all_assets_SMA_20_RSI_14 = []
    
    for idx, account in enumerate(accounts_list):
        try:
            tup = get_asset_hourly_SMA_20_RSI_14(f"{account['currency']}-USD", hours)
        except Exception as e:
            print('----------------------')
            print('There was an error at index #' + str(idx) + '. Asset: ' + account['currency'] + '-USD')
            print('Error message: ' + str(e))
            print('----------------------')
    
        asset_sma_20_rsi_14_dict = tup[1].tail().iloc[4, [0, 5, 6, 7]].to_dict()

        asset_sma_20_rsi_14_dict['product_id'] = tup[0]
    
        all_assets_SMA_20_RSI_14.append(asset_sma_20_rsi_14_dict)

    for idx, asset in enumerate(all_assets_SMA_20_RSI_14):
        if asset['RSI_14'] >= 70:
            assets_RSI_14_at_or_above_70.append(asset)
        # else:
        #     if idx == 0:
        #         print(f"{asset['product_id']} has an RSI below 70")
        #         print(f"RSI: {str(asset['RSI_14'])}")
        #         print("Checking next asset...")
        #         print()
        #         print('---------------------------')
        #     else:
        #         print()
        #         print(f"{asset['product_id']} has an RSI below 70")
        #         print(f"RSI: {str(asset['RSI_14'])}")
        #         print("Checking next asset...")
        #         print()
        #         print('---------------------------')
    return {"all_assets_SMA_20_and_RSI_14": all_assets_SMA_20_RSI_14, "assets_RSI_14_at_or_above_70": assets_RSI_14_at_or_above_70}

def create_asset(asset_id):
    asset = {
                  "uuid": str(generate_client_order_id()),
                  "name": f"{asset_id.upper()} Wallet",
                  "currency": asset_id.upper(),
                  "available_balance": {
                        "value": "0",
                        "currency": asset_id.upper()
                  },
                  "default": True,
                  "active": True,
                  "created_at": dt.now().strftime("%Y-%m-%dT%H:%M:%S.%f%zZ"),
                  "updated_at": dt.now().strftime("%Y-%m-%dT%H:%M:%S.%f%zZ"),
                  "deleted_at": None,
                  "type": "ACCOUNT_TYPE_CRYPTO",
                  "ready": True,
                  "hold": {
                        "value": "0",
                        "currency": asset_id.upper()
                  },
                  "retail_portfolio_id": "fa018cd4-479c-5a78-b676-533726262bb0",
                  "platform": "ACCOUNT_PLATFORM_CONSUMER"
            }
    
    return asset


def append_new_asset_to_json_file(asset_id):

    asset_name = asset_id
    modified_json_file_data = []

    with open('all_accounts_[Nov_28_2025].json', 'r') as file:
        json_file_data = json.load(file)
        
    for obj in json_file_data:
        modified_json_file_data.append(obj)
        
    modified_json_file_data.append(create_asset(asset_name))

    with open('all_accounts_[Nov_28_2025].json', 'w') as file:
        json.dump(modified_json_file_data, file, indent=4)

def add_new_asset_args_to_file(asset_id, price, price_dec, amount_dec, buy_amount, min_asst_bal, delay, has_decimal=True, main5_default='automatic'):
    if has_decimal:
        with open('bot_cmd_line_setup_with_manual_buy_sell_price_entry.txt', 'a') as file:
            file.write(f'\npython main3.py {price} {price_dec} {amount_dec} 1.025 0.025 {asset_id} 10.00 0.1 four four True True 1')
    
        with open('bot_cmd_line_setup.txt', 'a') as file:
            file.write(f'\npython main4.py {price_dec} {amount_dec} 1.025 0.025 {asset_id} 10.00 0.1 four four True True 1')
    
        with open('crypto_bot_recent_buys.txt', 'a') as file:
            file.write(f'\n\npython main3.py {asset_id} {price} 1.025 0.025 {buy_amount} {min_asst_bal} four four True True {delay}\n')
            file.write(f'python main3.py {asset_id} {price} 1.025 0.025 1.01 1.01 four four True True {delay}\n')
            file.write(f'python main4.py {asset_id} 1.025 0.025 {buy_amount} {min_asst_bal} four four True True {delay}\n')
            file.write(f'python main4.py {asset_id} 1.025 0.025 1.01 1.01 four four True True {delay}\n')
            file.write(f'\npython main5.py {asset_id} {main5_default} 0.05 {main5_default} {buy_amount} four {delay}\n')
            file.write(f'python main5.py {asset_id} {main5_default} 0.05 {main5_default} 1.01 four {delay}')
    else:
        with open('bot_cmd_line_setup_with_manual_buy_sell_price_entry.txt', 'a') as file:
            file.write(f'\npython main3.py {price} {price_dec} {amount_dec} 1.025 0.025 {asset_id} 10.00 0.1 two two True True 1')
    
        with open('bot_cmd_line_setup.txt', 'a') as file:
            file.write(f'\npython main4.py {price_dec} {amount_dec} 1.025 0.025 {asset_id} 10.00 0.1 two two True True 1')
    
        with open('crypto_bot_recent_buys.txt', 'a') as file:
            file.write(f'\n\npython main3.py {asset_id} {price} 1.025 0.025 {buy_amount} {min_asst_bal} two two True True {delay}\n')
            file.write(f'python main3.py {asset_id} {price} 1.025 0.025 1.01 1.01 two two True True {delay}\n')
            file.write(f'python main4.py {asset_id} 1.025 0.025 {buy_amount} {min_asst_bal} two two True True {delay}\n')
            file.write(f'python main4.py {asset_id} 1.025 0.025 1.01 1.01 two two True True {delay}\n')
            file.write(f'\npython main5.py {asset_id} {main5_default} 0.05 {main5_default} {buy_amount} two {delay}\n')
            file.write(f'python main5.py {asset_id} {main5_default} 0.05 {main5_default} 1.01 two {delay}')