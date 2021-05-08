from rest_framework import serializers
from .models import Price, Coin

class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = ('__all__')

class CoinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coin
        fields = ('__all__')

class AddCoinSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=64)
    amount = serializers.CharField(max_length=64)
    custom_price = serializers.CharField(max_length=64)

class SellCoinSerializer(serializers.Serializer):
    coin_id = serializers.CharField(max_length=64)
    amount = serializers.CharField(max_length=64)