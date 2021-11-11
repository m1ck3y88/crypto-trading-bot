import logging
import requests
import pprint

logger = logging.getLogger()



def get_products():

   response_object = requests.get("https://api.exchange.coinbase.com/products")

   print(response_object.status_code)

   for product in response_object.json():
      print(product)

get_products()