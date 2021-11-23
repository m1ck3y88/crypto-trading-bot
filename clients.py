import pandas as pd
import cbpro

import streamz
import streamz.dataframe

from holoviews.streams import Buffer


class CoinbaseProWebsocketClient(cbpro.WebsocketClient):
    CBPRO_DATE_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'

    def __init__(self, datastream=None, **kwargs):
        super().__init__(**kwargs)
        self.datastream = datastream
        self._set_update_function()

    def on_open(self):
        self.url = 'wss://ws-feed.pro.coinbase.com'
        self.message_count = 0

    def _set_update_function(self):
        # print(type(self.datastream))
        if isinstance(self.datastream, Buffer):
            print("Datastream of type: Buffer")
            self._updater_func = self.update_buffer

        elif isinstance(self.datastream, streamz.dataframe.DataFrame):
            print("Datastream of type: Streaming DataFrame")
            self.updater_func = self._update_stream_df

        elif isinstance(self.datastream, streamz.core.Stream):
            print("Datastream of type: Stream")
            self._updater_func = self._update_core_stream

        else:
            print(f"Unsupported Datastream of type: {type(self.datastream)}")
            self._updater_func = self._update_print

    def _update_print(self, **kwargs):
        price_val = kwargs.get('price', None)
        time_val = kwargs.get('time', None)
        print(f"DUDE {time_val} {price_val}")

    def _update_buffer(self, **kwargs):
        price_val = kwargs.get('price', None)
        time_val = kwargs.get('time', None)

        self.datastream.send(pd.DataFrame({         # .send() works for Buffer objects
                'timestamp':[time_val],
                'price'    :[price_val],
        }).set_index('timestamp'))

    def _update_stream_df(self, **kwargs):
        price_val = kwargs.get('price', None)
        time_val = kwargs.get('time', None)

        self.datastream.emit(pd.DataFrame({         # .emit() is for Stream objects
                'timestamp':[time_val],
                'price'    :[price_val],
        }).set_index('timestamp'))

    def _update_core_stream(self, **kwargs):
        price_val = kwargs.get('price', None)
        time_val = kwargs.get('time', None)

        self.datastream.emit([time_val, price_val])

    def on_message(self, msg):
        self.message_count += 1
        msg_type = msg.get('type', None)
        if msg_type == 'ticker':
            time_val = msg.get('time', None)
            time_val = pd.Timestamp(time_val)  # , format=self.CBPRO_DATE_FORMAT)

            price_val = msg.get('price', None)
            price_val = float(price_val)
            # print(time_val, price_val)

            self.updater_func(price=price_val, time=time_val)

    def on_close(self):
        print(f"<---Websocket connection closed--->\n\tTotal messages: {self.message_count}")


