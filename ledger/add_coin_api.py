from .models import Coin, Token, Price
import requests, decimal
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from datetime import datetime


def add_coin_api(coin_name, amount, custom_price, api_token):
    tokens = Token.objects.all().filter(key=api_token)
    owner = tokens[0].user

    coins = Coin.objects.all()
    coins = coins.filter(owner=owner)

    total_spent = 0
    total_coins = 0
    for coin in coins:
        if coin.name == coin_name and not coin.sold and not coin.merged:
            total_coins += coin.total_amount
            total_spent += coin.total_spent
            coin.date_sold = datetime.utcnow()
            coin.merged = True
            coin.save()

    total_amount = total_coins + (decimal.Decimal(str(amount)))
    coin = Coin(owner=owner, name=coin_name, amount=amount, total_amount=total_amount)

    symbol = coin.name[coin.name.find('(') + 1:coin.name.find(')')]
    coin_price = get_object_or_404(Price, symbol=symbol)

    coin.custom_price = decimal.Decimal(custom_price)
    

    if custom_price == '0':
        coin.custom_price = coin_price.price
    else:
        coin.custom_price = decimal.Decimal(custom_price)

    coin._purchase_price = coin.custom_price
        
    coin.total_spent = total_spent + (decimal.Decimal(str(amount)) * coin.purchase_price)
    coin._purchase_price = coin.total_spent / decimal.Decimal(str(total_amount))
    coin.current_price = coin_price.price

    coin.save()
    print('coin info', coin.name, coin.current_price)