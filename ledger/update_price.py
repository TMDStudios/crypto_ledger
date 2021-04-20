from .models import Coin, Price
import requests


def update_prices(price_data):
    price_update = price_data.split(',')
    coin_prices = Price.objects.all().filter(symbol=price_update[0])

    for coin_price in coin_prices:
        try:
            coin_price.price = float(price_update[1])
            print(f"{coin_price.symbol} = {coin_price.price}")
            try:
                coin_price.price_1h = float(price_update[2])
            except TypeError:
                pass
            coin_price.price_24h = float(price_update[3])
            coin_price.price_btc = float(price_update[4])
            coin_price.price_eth = float(price_update[5])
            coin_price.save()
        except KeyError:
            pass

    coins = Coin.objects.all()

    for coin in coins:
        symbol = coin.name[coin.name.find('(') + 1:coin.name.find(')')]
        if price_update[0] == symbol:
            coin.current_price = coin_price.price
            coin.save()
            # print(f"saved {coin.name} - {symbol} at id {coin.id}")

    return 'done'