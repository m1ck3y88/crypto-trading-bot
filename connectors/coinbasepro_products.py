import logging
import cbpro
from env.api_key import *
import pandas as pd
import talib as ta  # performs technical analysis on pandas Series or numpy arrays
import streamz
from streamz import Stream
from streamz.dataframe import DataFrame
import holoviews as hv
from holoviews import opts
from holoviews.streams import Buffer
from holoviews.plotting.links import RangeToolLink
from bokeh.models.tools import HoverTool

hv.extension('bokeh')

# from clients import CoinbaseProWebsocketClient

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


def get_live_products():
    product_ids = []

    for product in auth_client.get_products():
        product_ids.append(product['id'])

    return product_ids


def get_live_accounts():
    accounts = []

    for account in auth_client.get_accounts():
        accounts.append(account)

    return accounts


# for product in get_live_products():
#     print(product)

for account in get_live_accounts():
    if account['currency'] == 'JASMY':
        print(account)
