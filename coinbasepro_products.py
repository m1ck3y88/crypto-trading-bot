import logging
import requests


logger = logging.getLogger()



def get_products():

   response_object = requests.get("https://api-public.sandbox.exchange.coinbase.com/products")

   product_ids = []

   for product in response_object.json():
      product_ids.append(product['id'])

   return product_ids

print(get_products())
