from connectors.coinbasepro_products import *
import sys

# Args: asset_id, price, price_dec, amount_dec, buy_amount, min_asst_bal, delay, has_decimal=True, main5_default='automatic'

append_new_asset_to_json_file(sys.argv[1])

if len(sys.argv) == 9:
    add_new_asset_args_to_file(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], has_decimal=eval(sys.argv[8]))
elif len(sys.argv) == 10:
    add_new_asset_args_to_file(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], has_decimal=eval(sys.argv[8]), main5_default=sys.argv[9])
else:
    add_new_asset_args_to_file(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7])
                                                                                                             
    