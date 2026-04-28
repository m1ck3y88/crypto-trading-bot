# Algorithmic Python Cryptocurrency Trading Bot for the Coinbase Advanced Trade Platform

## Overview
Welcome to my Algorithmic Python Cryptocurrency Trading Bot for the Coinbase Advanced Trade Platform! This trading bot provides two primary algorithms for autonomously trading assets offered on the Coinbase Advanced Trade Platform. Although the bot is specifically written to trade cryptocurrency assets on the Coinbase Advanced Trade Platform, the core functionality of the algorithms can be implemented for autonomously trading any asset on any platform. The newest featured algorithm will always trade

The current code is the first public release of the alpha version and therefore updates will continue to be made for future realeases. Presently, I'm working on this project entirely on my own, so I appreciate everyone's patience as I refactor and optimize the code for future updates.

## Disclaimer:

This software is provided for educational and informational purposes only. I am not a licensed financial advisor, broker, or investment professional. The algorithmic trading bot and any related code are offered "as is," without warranty of any kind, express or implied.

Use of this software involves significant risk, including the potential loss of capital. You are solely responsible for any financial decisions or trades made using this code. Nothing in this project constitutes financial advice, investment recommendations, or an offer to buy or sell any financial instruments.

Before making any investment decisions, you should conduct your own research and consult with a qualified financial professional. By using this software, you agree that the developer assumes no liability for any losses, damages, or other consequences resulting from its use.

## Setup

First, download the zip file from this page and extract the contents in the directory of your choosing on your system. Ensure you have the latest version of Python installed (as this is a Python project), and then navigate into the project directory and install the Coinbase Advanced API Python SDK via `pip` by running the following command in the terminal/command line:

`pip3 install coinbase-advanced-py`

Click link for more information on the [Coinbase Advanced API Python SDK](https://github.com/coinbase/coinbase-advanced-py).
If you need to generate an API key(s) to trade programmatically on the Coinbase Advanced Platform click [here](https://docs.cdp.coinbase.com/advanced-trade/docs/getting-started).

Once you have the Coinbase Advanced API Python SDK installed, you can then immediately begin trading by choosing one of the `main` python scripts provided, with the necessary command line arguments, and then running it. Although there are 5 different scripts to choose from, `main4.py` is practically a duplicate of `main3.py` as well as `main7.py` a duplicate of `main5.py`, all with a few minor differences. I'll explain more below...

## The `main3.py` and `main4.py` Scripts

### The `main3.py` Script

The `main3.py` and `main4.py` scripts are simple algorithms that buy the amount of shares in correspondence with the specified dollar amount to be invested in the chosen asset, and the buy transaction will be triggered once the market price falls to or below the specified buy price. A sell transaction will then be triggered once the market price rises to or above the specified sell price. As the market price fluctuates, the bot will automatically adjust accordingly. The frequency that the bot checks the market price is determined by the amount of seconds you set it sleep before it checks again. 

The example below shows you what the command line setup might look like for trading $5 investments in Bitcoin for 5% profits:

`python3 main3.py btc 75000.00 1.05 0.05 5.00 50.00 four four True True 10`

1. The first argument, `python3`, is the interpreter.

2. The second argument, `main3.py` is the file name.

3. The third argument is the asset's "currency" property which identifies what the proper asset id will be when paired with your national fiat currence (e.g. BTC-USD). For Bitcoin, the currency property is "BTC".

4. The fourth argument is the price we are referencing to make a $5 investment once the market price falls at least 5% below that price. In this example we entered the price manually, but we can also have the bot calculate it for us automatically by setting this argument to `automatic`.

5. The fifth argument is the sell multiplier which will create a transaction to sell the corresponding investment once the market price climbs at least 5% above the initial buy price. This needs to be set manually in the above format. In this example, we chose 5%, so we would multiply the investment price by 1.05 to make a 5% profit.

6. The sixth argument is the buy price divider, which determines the percentage below the initial price at which the bot will make an investment. Unlike the previous argument, this argument can be calculated automatically by the bot by setting it to `automatic`, which will set investments to sell at the same percentage as the previous argument. However, if you choose to, you can manually set the percentage to any amount you choose but it needs to be in this format, with a zero-padded floating point number for percentages less than 100%.

7. The seventh argument is the amount you want each investment to be. In this example we chose $5 but you can have the bot buy exactly one share of the specified asset (provided you have the available funds), per investment, at whatever the market price is by setting this argument to the word `one` (not the numerical "1").

8. The eighth argument is the minimum cash threshold you choose to have before the bot will stop trading. In this example we set it to $50.00, which means that the bot will trade as long as the available cash balance is at least $50.00. This can be set to any number within your available cash balance.

9. The ninth argument has two functionalities in one:

    1. For assets without decimal precision (decimal places) in the amount per share set this to `one` or `two`  for limit buy orders or `five` or `six` for market buy orders

        - `python3 main3.py shib 0.00000599 1.05 0.05 5.00 50.00 eight Fasle True 10`

    2. For assets with decimal precision (decimal places) in the amount per share set this to `three` or `four` for limit buy orders or `seven` or `eight` for market buy orders

        - `python3 main3.py btc 75000.00 1.05 0.05 5.00 50.00 four four True True 10`

    The second example above is for a limit buy order of $5 worth of Bitcoin once the price falls 5% below $75,000 per share ($71,250), which would come out to approximately 0.00007018 Bitcoin. Bitcoin allows up to 8 decimal places for its decimal precision, but this does not necessarily apply to all assets, as some assets have no decimal precision like the meme coin Shiba Inu. The first example above shows what the command line might look like if you were to place a market buy order of $5 of Shiba Inu once the price falls 5% below $0.00000599 per share (about 0.00000569 Shiba Inu), which would be approximately 878,734 Shiba Inu. Coinbase will round the purchase amount to an integer since there is no decimal precision. All of this is handled by the bot provided you provide the right arguments for the transaction you want to make, according to the instructions above.
    
    This argument tells the bot what type of decimal precision the asset you are investing in has as well as what type of buy order you are placing. Ultimately, this argument was originally intended for prototyping purposes and will eventually be removed in a future release due to its tedious and complex nature. Nevertheless, since the code has not been refactored to allow the complete removal of this argument, follow the instructions above to avoid breaking the bot.

10. The same instructions as the previous argument apply to this argument but for limit sell and market sell orders.

11. This argument tells the bot whether you want to make a limit buy order or a market buy order. It corresponds to the 9th argument so if you chose `one`, `two`, `three` or `four` for the 9th argument, then you would set this to `True` for a limit buy order. Otherwise, if you chose `five`, `six`, `seven` or `eight` for the 9th argument, you would set this argument to `False` for market buy order

12. The same instructions as the previous argument apply to this argument but for limit sell and market sell orders.

    Just ast mentioned above about the 9th and 10th arguments, the 11th and 12th arguments are for prototyping purposes and will also be removed in a future release, but follow the current instructions, as listed, to avoid running into errors

13. This argument is the amount of time in seconds to have the bot wait before it loops to check the price again and potentially make an investment or sell for a profit. This can be an integer like in the examples above or you can even set it to a floating point number to have the bot wait a fraction of a second. Example: `0.25` (Setting this argument to this value would have the bot check every $\frac{1}{4}$ of a second).

### The `main4.py` Script

Since this script is practically a copy of `main3.py`, with just a few lines differing from that script, I won't go into detail about it. All that you need to know to properly use this script is that there is only one less argument which is the "price" argument which would be the 4th argument of the `main3.py` script. Basically, you would use this script if you want to just start making investments based on the current market price, without manually entering a command to determine where the bot begins making investments. I know it's typically a bad practice to have repeated code, but as stated before, this project is still in its very early stages and a long ways from being complete. Nevertheless, the bot will do exactly what you want it to do provided you chose the right script according to these instructions. Below is an example of what the command line may look like using the same arguments that we used in the very first example above for investing in Bitcoin, but of course just with no price argument:

`python3 main4.py btc 1.05 0.05 5.00 50.00 four four True True 10`

All the same instructions apply to this script as the one above, except that the bot will just atonomously fetch the current market price and then calculate the buy price based on that information along with the buy price divider percentage argument you chose.

### The `main5.py` Script

This script has a significantly more sophisticated algorithm that will not only make investments at whatever percentage you choose below the specified market price, but will also directly place a corresponding sell order for a precise profit at the specified percentage or better, for each individual investment. This is acheived by each investment being stored in a list to keep it in memory, and it will not be removed from memory until the bot confirms it is filled, always placing a corresponding sell transaction for a profit at your specified percentage before the original investment is removed from memory. This script's command line arguments also follow all of the same instructions as the above listed scripts with just a few less arguments. Below is an example with Bitcoin once again:

`python3 main5.py btc automatic 0.05 automatic one four 10`

### Quick Overview of Command Line Arguments

 - The first two arguments, `python3` and `main5.py`, are always the interpreter and the file name, respectively.

 - The third argument, `btc`, is the asset's "currency" property, and identifies the asset you want to invest in just like the scripts above.
 
 - The fourth argument is the price, with which you can enter in manually, or have the bot identify automatically by setting the argument to `automatic` as in the example above. You also have three additional options that are not offered in the `main3.py` or `main4.py` scripts, which are as follows:

    1. If this argument is set to `high`, then the bot will calculate the buy price to be whatever specified percentage below the current hourly candle's high is for the specified asset

    2. If this argument is set to `open`, then the bot will calculate the buy price to be whatever specified percentage below the current hourly candle's opening price for the specified asset.

    3. If this argument is set to `low`, then the bot will calculate the buy price to be whatever specified percentage below the current hourly candle's low for the specified asset.

 - The fifth argument, `0.05`, is the buy price divider, which determines the percentage below the initial price at which the bot will make an investment. This argument actually comes right before the sell price multiplier argument, which is the inverse of the `main3.py` and `main4.py` scripts listed above. Keep this in mind and remember that it needs to written in this format, with zero-padding if you choose a percentage below 100%.

 - The sixth argument is the sell price multiplier, which will create a transaction to sell the corresponding investment once the market price climbs at least 5% above the initial buy price, again the same as it does in the `main3.py` and `main4.py` scripts above.

 - The seventh argument is the investment amount, which like the `main3.py` and `main4.py` scripts can be set to `one` to make and investment of exactly one share of the asset at whatever the current buy price is set to, or you can manually enter in the dollar amount you wish to invest as a floating point number (or and integer).

 - The eighth argument is just like the ninth argument in the `main3.py` and `main4.py` scripts, and let's the bot know whether the asset has decimal precision or not. The main difference in this script is that it is written to only make limit orders to function as intended, so this argument will apply to both buys and sells, hence why there isn't a duplicate argument for both transaction types like in the above scripts. This argument is for prototyping purposes and will eventually be removed, again just as the same argument(s) in the above scripts, but for now, use `two` for non-decimal precision assets and `four` for assets with decimal precision.

 - The ninth and last argument is the amount of seconds to have the bot wait before it loops and checks to make an investment and/or sell for a profit. This can be an integer or a floating point number to wait just a fraction of a second.

### The `main7.py` Script

Just as the first two scripts are practically copies of each other, this script is a copy of `main5.py` and all the arguments are exactly the same. It's just the code that slightly differs. The code in `main5.py`, starting on lines 286 and 388, has blocks of logic that bump the bot's `delay` variable up to 2 $\frac{1}{2}$ minutes (150 seconds) once the available balance drops to 75% (or lower) of the total portfolio balance, and 5 minutes (300 seconds) once the available balance drops below 50% (or lower) of the total portfolio balance, respectively. This logic is commented out in the `main7.py` script. I know that all of this could be remedied by simply making the code more modular through functional and/or Object Oriented Programming, but I just haven't quite got around to that yet. Again, all this code is at an early prototype stage and this will all eventually be fixed in later releases. Below is a preview of the aforementioned code blocks:

`main5.py` starting @lines 286 and 388:

```python
            if available_balance <= dynamic_portfolio_balance * 0.75 and available_balance > dynamic_portfolio_balance * 0.5:

                if available_balance > initial_portfolio_balance:

                    delay = float(sys.argv[7])
                    
                else:

                    delay = 150

                buy_price_divdr = 0.075

                sell_price_mltplr = 1.05

            elif available_balance <= dynamic_portfolio_balance * 0.5:

                if available_balance > initial_portfolio_balance:

                    delay = float(sys.argv[7])
                    
                else:

                    delay = 300

                buy_price_divdr = 0.1
                
                sell_price_mltplr = 1.075
```

`main7.py` also starting @lines 286 and 388:

```python
                # if available_balance > initial_portfolio_balance:

                #     delay = float(sys.argv[7])
                    
                # else:

                #     delay = 150

                buy_price_divdr = 0.075

                sell_price_mltplr = 1.05

            elif available_balance <= dynamic_portfolio_balance * 0.5:

                # if available_balance > initial_portfolio_balance:

                #     delay = float(sys.argv[7])
                    
                # else:

                #     delay = 300

                buy_price_divdr = 0.1
                
                sell_price_mltplr = 1.075
```

### Setting Up the `api_key.py` File

Inside the included `env` directory is a copy of an `api_key_example.txt` file. Create an actual `api_key.py` file inside this directory, copy the code from the example file and replace the `api_key` and `api_secret` variables with your actual API key and API Secret. 