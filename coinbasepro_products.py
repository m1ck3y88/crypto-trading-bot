import logging
import cbpro
from api_key import sandbox_api_key, sandbox_api_secret, sandbox_api_pass


logger = logging.getLogger()

auth_client = cbpro.AuthenticatedClient(sandbox_api_key, sandbox_api_secret, sandbox_api_pass,
                                        api_url="https://api-public.sandbox.pro.coinbase.com")


# print(auth_client.get_accounts())
currency_id = 'dec357c4-0b6d-4c84-90a2-9b5df1d21613'  # USD

def get_auth_products():

    product_ids = []

    for product in auth_client.get_products():

        product_ids.append(product['id'])

    return product_ids


print(get_auth_products())  # ['BTC-GBP', 'LINK-USDC', 'ETH-BTC', 'BAT-USDC', 'BTC-EUR',
                            # 'LINK-USD', 'BTC-USD', 'XRP-BTC', 'XRP-USD', 'XRP-GBP', 'XRP-EUR']







