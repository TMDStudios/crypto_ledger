from rest_framework import serializers


class CoinSerializer(serializers.Serializer):
    coin = serializers.CharField()
    price = serializers.FloatField()