from rest_framework import serializers
from .models import Price, Coin

class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = ('name', 'price')

class CoinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coin
        fields = ('name', 'date_bought', 'purchase_price', 'total_amount', 'total_value')