from env.api_key import *
import cbpro

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
