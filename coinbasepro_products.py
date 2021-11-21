import logging
import cbpro
from api_key import sandbox_api_key, sandbox_api_secret, sandbox_api_pass, api_key, api_secret, api_pass

logger = logging.getLogger()

auth_sandbox_client = cbpro.AuthenticatedClient(sandbox_api_key, sandbox_api_secret, sandbox_api_pass,
                                                api_url="https://api-public.sandbox.pro.coinbase.com")

auth_client = cbpro.AuthenticatedClient(api_key, api_secret, api_pass)


def get_sandbox_products():
    product_ids = []

    for product in auth_sandbox_client.get_products():
        product_ids.append(product['id'])

    return product_ids


def get_sandbox_accounts():
    accounts = []

    for account in auth_sandbox_client.get_accounts():
        accounts.append(account)

    return accounts


class TestWebsocketClient(cbpro.WebsocketClient):
    def on_open(self):
        self.url           = 'wss://ws-feed.pro.coinbase.com/'
        self.message_count = 0

    def on_message(self, msg):
        self.message_count += 1
        msg_type = msg.get('type', None)
        if msg_type == 'ticker':
            time_val   = msg.get('time', ('-'*27))
            price_val  = msg.get('price', None)
            price_val  = float(price_val) if price_val is not None else 'None'
            product_id = msg.get('product_id', None)

            print(f"{time_val:30} {price_val:.3f} {product_id}\tchannel type:{msg_type}")

    def on_close(self):
        print(f"<---Websocket connection closed--->\n\tTotal messages: {self.message_count}")

stream = TestWebsocketClient(products=['BTC-USD'], channels=['ticker'])
# stream.start()

# while stream.message_count < 200:
#
#     continue
#
# else:
#     stream.close()
