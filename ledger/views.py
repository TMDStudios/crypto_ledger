from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, JsonResponse
import requests, decimal
from .models import Coin, Price, Profile
from .forms import CoinForm, SellForm, SettingsForm
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from datetime import datetime
from django.forms.models import model_to_dict
from django.contrib.auth.models import User
from .serializers import PriceSerializer, CoinSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

import schedule
import time

def customize_ticker(owner):
    prices = Price.objects.all()
    prices = prices.order_by('name')
    selected_ticker_prices = []
    if owner.is_authenticated:
        user_profile = Profile.objects.all().filter(user=owner)

        if not user_profile:
            user_profile = Profile(user=owner, ticker_prices="")
            user_profile.save()
        user_profile = Profile.objects.all().filter(user=owner)[0]

        filtered_ticker_prices = user_profile.ticker_prices.split(',')
        
        for price in prices:
            if price.symbol in filtered_ticker_prices:
                selected_ticker_prices.append(price)

    return selected_ticker_prices

def home(request):
    context = {}
    form = SellForm()
    limit_history = 0
    overall_total = 0
    current_profit = 0
    overall_profit = 0
    if request.user.is_authenticated:
        owner = get_object_or_404(User, id=request.user.id)
        context['selected_ticker_prices'] = customize_ticker(owner)
        user_settings = Profile.objects.all()
        user_settings = user_settings.filter(user=owner)[0]
        context['dark_mode'] = user_settings.dark_mode
        limit_history = user_settings.limit_history
        coins = Coin.objects.all().filter(owner=owner)
        coins = coins.order_by('-id')
        context['coins'] = coins

        for coin in coins:
            coin.price_difference = coin.current_price / coin.purchase_price * decimal.Decimal('100') - decimal.Decimal('100')
            current_price_decimal = decimal.Decimal(str(coin.current_price))
            coin.value = current_price_decimal * coin.total_amount
            coin.total_profit = coin.current_price * coin.total_amount - coin.purchase_price * coin.total_amount

            coin.total_value = current_price_decimal * coin.total_amount
            if not coin.sold and not coin.merged:
                overall_total += coin.total_value
                current_profit += coin.total_profit
            if coin.sold:
                overall_profit += coin.gain

            coin.save()

        if limit_history > 0:
            inactive_coins = coins.filter(owner=owner).exclude(date_sold=None)
            inactive_coins = inactive_coins.order_by('-date_sold')[:user_settings.limit_history]
        else:
            inactive_coins = coins.order_by('-date_sold')

        context['inactive_coins'] = inactive_coins

    prices = Price.objects.all()
    prices = prices.order_by('name')

    context['prices'] = prices
    context['form'] = form
    context['overall_total'] = overall_total
    context['current_profit'] = current_profit
    context['overall_profit'] = overall_profit

    return render(request, 'home.html', context)


def add_coin(request):
    if request.method == 'POST':
        form = CoinForm(request.POST)
        if form.is_valid():
            owner = get_object_or_404(User, id=request.user.id)
            name = form.cleaned_data['name']
            amount = form.cleaned_data['amount']
            custom_price = form.cleaned_data['custom_price']

            coins = Coin.objects.all()
            coins = coins.filter(owner=owner)

            total_spent = 0
            total_coins = 0
            for coin in coins:
                if coin.name == name and not coin.sold and not coin.merged:
                    total_coins += coin.total_amount
                    total_spent += coin.total_spent
                    coin.date_sold = datetime.utcnow()
                    coin.merged = True
                    coin.save()

            total_amount = total_coins + amount
            coin = Coin(owner=owner, name=name, amount=amount, total_amount=total_amount)

            symbol = coin.name[coin.name.find('(') + 1:coin.name.find(')')]
            coin_price = get_object_or_404(Price, symbol=symbol)

            coin.custom_price = decimal.Decimal(str(custom_price))
            

            if custom_price == 0:
                coin.custom_price = coin_price.price
            else:
                coin.custom_price = decimal.Decimal(str(custom_price))

            coin._purchase_price = coin.custom_price
                
            coin.total_spent = total_spent + (amount * coin.purchase_price)
            coin._purchase_price = coin.total_spent / decimal.Decimal(str(total_amount))
            coin.current_price = coin_price.price

            coin.save()

            return redirect('home')
        else:
            issue = form.errors
            usr = request.user.id
            return render(request, 'add_coin.html', {'issue': issue, 'usr': usr})
    else:
        form = CoinForm()

    return render(request, 'add_coin.html', {'form': form})


def sell_coin(request, id):
    coin = get_object_or_404(Coin, id=id)
    name = coin.name
    form = SellForm()

    coins = Coin.objects.all()
    owner = get_object_or_404(User, id=request.user.id)
    coins = coins.filter(owner=owner)

    for c in coins:
        if c.name == name:
            c.total_amount += c.amount

    if request.method == 'POST':
        form = SellForm(request.POST)
        if form.is_valid():
            if id == coin.id:
                coin.sell_amount = form.cleaned_data['sell_amount']

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

    return redirect('home')

def delete_coin(request, id):  
    if id == 0:
        owner = get_object_or_404(User, id=request.user.id)
        user_settings = Profile.objects.all()
        user_settings = user_settings.filter(user=owner)[0]
        coins = Coin.objects.all()
        coins = coins.order_by('-id')
        coins = coins.filter(owner=owner)
        if request.method == "POST":
            for coin in coins:
                if coin.merged or coin.sold:
                    coin.delete()
            return redirect('home')
        context = {
            'all_coins': 'all_coins',
            'dark_mode': user_settings.dark_mode
        }
    else:
        coin = get_object_or_404(Coin, id=id)
        if request.method == "POST":
            coin.delete()
            return redirect('home')
        context = {
            'deleted_coin': coin
        }
    return render(request, 'delete_coin.html', context)

def coin_details(request, id):
    form = SellForm()
    coin_name = get_object_or_404(Coin, id=id)
    name = coin_name.name
    symbol = name[name.find('(') + 1:name.find(')')]
    context = {}
    owner = get_object_or_404(User, id=request.user.id)
    coins = Coin.objects.all()
    coins = coins.order_by('-id')
    coins = coins.filter(owner=owner)
    coins = coins.filter(name=name)
    context['coins'] = coins
    context['form'] = form
    context['symbol'] = symbol
    context['name'] = name.split(" ")[0]

    user_settings = Profile.objects.all()
    user_settings = user_settings.filter(user=owner)[0]
    context['dark_mode'] = user_settings.dark_mode

    return render(request, 'coin_details.html', context)

def general_details(request, id):
    coin = get_object_or_404(Price, id=id)
    symbol = coin.symbol
    context = {}
    context['symbol'] = symbol
    context['name'] = coin.name.split(" ")[0]

    return render(request, 'general_details.html', context)

def all_prices(request):
    context = {}
    if request.user.is_authenticated:
        owner = get_object_or_404(User, id=request.user.id)
        context['selected_ticker_prices'] = customize_ticker(owner)
        user_settings = Profile.objects.all()
        user_settings = user_settings.filter(user=owner)[0]
        context['dark_mode'] = user_settings.dark_mode
    coins = Price.objects.all()
    coins = coins.order_by('name') 

    prices = Price.objects.all()
    prices = prices.order_by('name')
    context['prices'] = prices

    if request.method == "POST":
        coin_name = request.POST.get('coin_name')
        price_usd = request.POST.get('price_usd')
        price_1h = request.POST.get('price_1h')
        price_24h = request.POST.get('price_24h')
        price_btc = request.POST.get('price_btc')
        price_eth = request.POST.get('price_eth')

        if coin_name:
            if coin_name == "Asc":
                coins = coins.order_by('name') 
            elif coin_name == "Desc":
                coins = coins.order_by('-name') 
        if price_usd:
            if price_usd == "Asc":
                coins = coins.order_by('price') 
            elif price_usd == "Desc":
                coins = coins.order_by('-price') 
        if price_1h:
            if price_1h == "Asc":
                coins = coins.order_by('price_1h') 
            elif price_1h == "Desc":
                coins = coins.order_by('-price_1h') 
        if price_24h:
            if price_24h == "Asc":
                coins = coins.order_by('price_24h') 
            elif price_24h == "Desc":
                coins = coins.order_by('-price_24h') 
        if price_btc:
            if price_btc == "Asc":
                coins = coins.order_by('price_btc') 
            elif price_btc == "Desc":
                coins = coins.order_by('-price_btc') 
        if price_eth:
            if price_eth == "Asc":
                coins = coins.order_by('price_eth') 
            elif price_eth == "Desc":
                coins = coins.order_by('-price_eth') 

        context['coins'] = coins
        return render(request, 'all_prices.html', context)

    context['coins'] = coins

    return render(request, 'all_prices.html', context)

def settings(request):
    if request.method == 'POST':
        form = SettingsForm(request.POST)
        if form.is_valid():
            owner = get_object_or_404(User, id=request.user.id)
            selected_ticker_prices = form.cleaned_data['ticker_prices']
            user_settings = Profile.objects.all()
            user_settings = user_settings.filter(user=owner)[0]
            dark_mode = form.cleaned_data['dark_mode']
            limit_history = form.cleaned_data['limit_history']

            if not user_settings:
                user_settings = Profile(user=owner, ticker_prices="")
                user_settings.save()

            user_settings.ticker_prices = ""
            user_settings.dark_mode = dark_mode
            user_settings.limit_history = limit_history
            user_settings.save()

            split_prices = ""
            for i in selected_ticker_prices:
                if i.isalpha() or i == '(' or i == ')' or i == ',':
                    split_prices += i

            price_list = split_prices.split(',')

            for price in price_list:
                user_settings.ticker_prices += f"{price[price.find('(') + 1:price.find(')')]},"
                user_settings.save()

            return redirect('home')
        else:
            issue = form.errors
            usr = request.user.id
            return render(request, 'settings.html', {'issue': issue, 'usr': usr})
    else:
        owner = get_object_or_404(User, id=request.user.id)
        user_settings = Profile.objects.all()
        user_settings = user_settings.filter(user=owner)[0]
        dark_mode = user_settings.dark_mode
        if dark_mode:
            form = SettingsForm(initial={'dark_mode': True, 'limit_history': user_settings.limit_history})
        else:
            form = SettingsForm(initial={'dark_mode': False, 'limit_history': user_settings.limit_history})

    return render(request, 'settings.html', {'form': form, 'dark_mode': dark_mode})

def get_prices(request):
    coins = Price.objects.all()
    serializer = PriceSerializer(coins, many=True)
    return JsonResponse(serializer.data, safe=False)

def get_user_ledger(request):
    if request.user.is_authenticated:
        owner = get_object_or_404(User, id=request.user.id)
        coins = Coin.objects.filter(owner=owner, sold=False, merged=False)
        serializer = CoinSerializer(coins, many=True)
        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({}, safe=False)