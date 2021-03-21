from celery import shared_task
from .models import Coin, Price
import requests
from time import sleep


@shared_task
def update_prices(update_round):
    coins = Coin.objects.all()
    coin_prices = Price.objects.all()

    group = (
        ('BTC', 'BCH', 'DAI', 'DASH', 'DOGE', 'LTC', 'XMR', 'NANO', 'PAXG', 'XRP',
        'XLM', 'ZEC', 'ALGO', 'ADA', 'ATOM', 'EOS', 'ETH', 'ETC', 'DOT'),
        ('KSM', 'LSK', 'ICX', 'OMG', 'XTZ', 'TRX', 'WAVES', 'REP', 'BAL', 'COMP', 
        'CRV', 'GNO', 'KAVA', 'KNC', 'SNX', 'LINK', 'FIL', 'OXT', 'SC'),
        ('STORJ', 'BAT', 'USDT', 'MLN', 'GRT')
    )

    for coin_price in coin_prices:
        if coin_price.symbol in group[update_round]:
            api_url = 'https://data.messari.io/api/v1/assets/'+coin_price.symbol.lower()+'/metrics'
            response = requests.get(api_url)
            data = response.json()

            try:
                coin_price.symbol = str(data['data']['symbol'])
                coin_price.price = float(data['data']['market_data']['price_usd'])
                coin_price.price_1h = float(data['data']['market_data']['percent_change_usd_last_1_hour'])
                coin_price.price_24h = float(data['data']['market_data']['percent_change_usd_last_24_hours'])
                coin_price.price_btc = float(data['data']['market_data']['price_btc'])
                coin_price.price_eth = float(data['data']['market_data']['price_eth'])
                coin_price.save()
            except KeyError:
                pass

        for coin in coins:
            symbol = coin.name[coin.name.find('(') + 1:coin.name.find(')')]
            if coin_price.symbol == symbol:
                coin.current_price = coin_price.price
                coin.save()

    print(f'Prices updated: {group[update_round]}')
    return 'done'