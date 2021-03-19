from rest_framework import serializers
from .models import Price

class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = ('name', 'price')