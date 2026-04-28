from connectors.coinbasepro_products import *
from pathlib import Path
import time
import ast
import sys
import os

if __name__ == '__main__':

    # Live Account Limit Buy/Limit Sell Algorithm
    cur = 'USD'
    txt_filename = 'bot_cmd_line_setup_with_manual_buy_sell_price_entry.txt'
    json_filename = 'all_accounts_[Nov_18_2025][2].json'
    all_accounts = get_all_assets(json_filename)
    # usd_wallet = [wallet for wallet in all_accounts if wallet['currency'] == cur][0]
    asset_args = get_asset_args_setup(get_assets_args_setup_list(txt_filename), sys.argv[1])
    price_dec_plcs = int(asset_args[3])
    amnt_dec_plcs = int(asset_args[4])
    sell_price_mltplr = float(sys.argv[2])

    coin = sys.argv[1].upper()
    coin_wallet = [wallet for wallet in all_accounts if wallet['currency'] == coin][0]
    asset_id = '{}-{}'.format(coin, cur)
    websocket_data_list = []
    # maker_fee = 0.0025
    # fee = 0.0040
    delay = float(sys.argv[3])
    # count = 0
    
    filled_buy_order_list = []
    file_list = []

    root_dir = Path('.')
    file_paths = root_dir.iterdir()

    for path in file_paths:
        if path.is_file() and 'flld_buy_ordrs' in path.parts[0] and '.txt' in path.parts[0]:
            file_list.append(path.parts[0])


    def quick_sell(filename, lst):

        if not os.path.exists(filename):

            raise FileNotFoundError(f'File {filename} does not exist!')
        
        else:

            with open(filename, 'r') as file:
                lst = ast.literal_eval(file.read())

        price = float(client.get_product(asset_id).to_dict()['price'])

        if len(lst) >= 1:

            for order in lst:

                size = float(order['order_configuration']['limit_limit_gtc']['base_size'])

                order_price = float(order['order_configuration']['limit_limit_gtc']['limit_price'])

                order_sell_price = float(('{:.' + str(price_dec_plcs) + 'f}').format(order_price * sell_price_mltplr))

                if price > order_sell_price and float(coin_wallet['available_balance']['value']) >= order_sell_price:
                
                    # Limit Sell Order (Max)
                    last_sell_ordr = client.limit_order_gtc_sell(client_order_id=str(generate_client_order_id()), product_id=asset_id, base_size=str(size), limit_price= str(price))
                    
                    with open(f'[{dt.now().strftime("%b_%d_%Y")}]last_sell_order.json', 'w') as file:

                        json.dump(last_sell_ordr.to_dict(), file, indent=6)
                else:
                                
                    # Limit Sell Order (Max)
                    last_sell_ordr = client.limit_order_gtc_sell(client_order_id=str(generate_client_order_id()), product_id=asset_id, base_size=str(size), limit_price=str(order_sell_price))
                    
                    with open(f'[{dt.now().strftime("%b_%d_%Y")}]last_sell_order.json', 'w') as file:

                        json.dump(last_sell_ordr.to_dict(), file, indent=6)

            lst = []
            with open(filename, 'w') as file:
                file.write(str(lst))
            
        else:
            print(f'File {filename} is empty!')

    while True:

        for file in file_list:
            if asset_id in file:
                quick_sell(file, filled_buy_order_list)

        print(f'Checking again in {delay} seconds')
        time.sleep(delay)

    # def on_message(msg):
    #     global websocket_data_list
    #     file_name = f'websocket_data_[{dt.now().strftime("%b_%d_%Y")}].json'
    #     message_data = json.loads(msg)
    #     websocket_data_list.append(message_data)
    #     # print(json.dumps(websocket_data_list, indent=4))
    #     with open(file_name, 'w') as file:
    #         json.dump(websocket_data_list, file, indent=4)

    # ws_client = WSClient(api_key=creds[0], api_secret=creds[1], on_message=on_message)

    # open the connection and subscribe to the ticker and heartbeat channels for asset_id
    # ws_client.open()
    # ws_client.ticker(product_ids=[asset_id])
    # ws_client.user(product_ids=[asset_id])
    # ws_client.heartbeats()
    # ws_client.subscribe(product_ids=[asset_id], channels=["ticker", "user"])

    # wait 10 seconds
    # time.sleep(5)

    # unsubscribe from the ticker channel and heartbeat channels for asset_id, and close the connection
    # ws_client.unsubscribe(product_ids=[asset_id], channels=["ticker", "user"])
    # ws_client.ticker_unsubscribe(product_ids=[asset_id])
    # ws_client.heartbeats_unsubscribe()
    # ws_client.close()
        
        # print(json.dumps(list(filled_buy_order_list), indent=4))
    # filled_orders = client.get_fills(product_ids=['FIS-USD']).to_dict()

    # print(json.dumps(filled_orders, indent=4))

    # price = float(client.get_product(asset_id).to_dict()['price'])


        
    
