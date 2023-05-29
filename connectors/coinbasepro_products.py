import logging
import cbpro
from env.api_key import *
# import pandas as pd
# import talib as ta  # performs technical analysis on pandas Series or numpy arrays
# import streamz
# from streamz import Stream
# from streamz.dataframe import DataFrame
# import holoviews as hv
# from holoviews import opts
# from holoviews.streams import Buffer
# from holoviews.plotting.links import RangeToolLink
# from bokeh.models.tools import HoverTool

# hv.extension('bokeh')

# from clients import CoinbaseProWebsocketClient

logger = logging.getLogger()

auth_sandbox_client = cbpro.AuthenticatedClient(sandbox_api_key, sandbox_api_secret, sandbox_api_pass,
                                                api_url="https://api-public.sandbox.exchange.coinbase.com")

auth_client = cbpro.AuthenticatedClient(api_key, api_secret, api_pass)


def get_sandbox_products():

    for product in auth_sandbox_client.get_products():
        yield product['id']


def get_sandbox_accounts():

    for account in auth_sandbox_client.get_accounts():
        yield account


def get_live_products():

    for product in auth_client.get_products():
        yield product['id']


def get_live_accounts():

    for account in auth_client.get_accounts():
        yield account


# def compute_rsi(emitted_vals):
#     # assumes emitted_vals is a list of pandas Dataframes
#     master_df = pd.concat([df for df in emitted_vals])
#
#     rsi_series = ta.RSI(master_df['price'])
#
#     rsi_val = rsi_series[-1]
#     t_val = master_df.index[-1]
#     return pd.DataFrame({'timestamp': [t_val], 'rsi': [rsi_val]}).set_index('timestamp', drop=True)
#
#
# source = Stream()
#
# sample_df = pd.DataFrame({'timestamp': [], 'price': []}).set_index('timestamp', drop=True)
# sdf = DataFrame(source, example=sample_df)
#
# sample_rsi_df = pd.DataFrame({'timestamp': [], 'rsi': []}).set_index('timestamp', drop=True)
# rsi_buffer = Buffer(sample_rsi_df, length=100)
# rsi_stream = Stream(
#     upstream=source
# ).sliding_window(
#     15,
#     return_partial=False
# ).map(
#     compute_rsi
# ).sink(
#     rsi_buffer.send
# )
#
# product_to_stream = 'BTC-USD'
# socket_stream = CoinbaseProWebsocketClient(sdf, products=['BTC-USD'], channels=['ticker'])
#
# socket_stream.start()
#
# # Define some interactivity tools for the graph
# hover = HoverTool(
#     tooltips=[
#         ('time', '@timestamp{%H:%M:%S'),
#         ('price', '@price{($ 0.00)}'),
#     ],
#     formatters={
#         '@timestamp': 'datetime'
#     }
# )
#
# price_chart = hv.DynamicMap(
#     hv.Curve,
#     streams=[Buffer(sdf, length=100)]
# ).opts(
#     title=f'Live {product_to_stream} Chart',
#     padding=0.05,
#     width=800,
#     height=300,
#     show_grid=True,
#     tools=[hover], # add the interactive tools we defined above
# )
#
# mean_chart = hv.DynamicMap(
#     hv.Curve,
#     streams=[Buffer(sdf['price'].rolling(50).mean(), length=100)],
# ).opts(
#     tools=[hover]
# )
#
# rsi_chart = hv.DynamicMap(
#     hv.Curve,
#     streams=[rsi_buffer]
# ).opts(
#     title='',
#     width=800,
#     height=150,
#     axiswise=True,
# )
#
# table_chart = hv.DynamicMap(
#     hv.Table,
#     streams=[Buffer(sdf, length=10)]
# ).opts(padding=0.1, width=300)
#
# rtlink = RangeToolLink(rsi_chart, price_chart)
# combined_chart = ((price_chart*mean_chart) + rsi_chart).opts(shared_axes=True, merge_tools=False).cols(1)
