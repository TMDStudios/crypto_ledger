from .models import Coin, Token, Price
import decimal
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from datetime import datetime


def sell_coin_api(id, amount, api_token):
    tokens = Token.objects.all().filter(key=api_token)

    coin = get_object_or_404(Coin, id=id)
    name = coin.name

    coins = Coin.objects.all()
    owner = tokens[0].user
    coins = coins.filter(owner=owner)

    for c in coins:
        if c.name == name:
            c.total_amount += c.amount

    coin.sell_amount = decimal.Decimal(str(amount))

    if coin.sell_amount <= coin.total_amount and coin.sell_amount > 0:
        coin.sold = True
        coin.date_sold = datetime.utcnow()
        coin.sell_price = coin.current_price
        coin.gain = coin.sell_price * coin.sell_amount - coin.purchase_price * coin.sell_amount
        coin.total_amount = coin.total_amount - coin.sell_amount
        coin.total_spent -= coin.sell_amount * coin.purchase_price
        coin.save()

    if coin.total_amount > 0:
        coins = Coin.objects.all()
        coins = coins.filter(owner=owner)
        open_order_exists = False

        for coin_order in coins:
            if coin_order.name == name and not coin_order.sold and not coin_order.merged:
                open_order_exists = True
                coin_order.amount = coin.total_amount
                coin_order.total_amount = coin.total_amount
                coin_order.save()

        if not open_order_exists:
            coin.pk = None
            coin.sold = False
            coin.date_sold = None                
            coin.value = coin.total_amount * coin.current_price
            coin.total_value = coin.total_amount * coin.current_price
            coin.price_difference = coin.current_price / coin.purchase_price * decimal.Decimal('100') - decimal.Decimal('100')
            coin.save()
