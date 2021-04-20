from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
import requests, decimal


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Profile(models.Model):
    objects = models.Manager()
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    ticker_prices = models.TextField(default="", blank=True, null=True)
    dark_mode = models.BooleanField(default=True, blank=True)
    limit_history = models.IntegerField(default=0, null=True, blank=True)
    transaction_view = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return str(self.user)


class Date(models.Model):
    objects = models.Manager()  # gets rid of linter (query) issues
    last_update = models.DateTimeField(default=datetime.utcnow())
    update_round = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return str(self.last_update)
    


class Price(models.Model):
    objects = models.Manager()  # gets rid of linter (query) issues
    symbol = models.CharField(max_length=50, null=True, unique=True)
    name = models.CharField(max_length=50, null=True)
    price = models.DecimalField(max_digits=16, decimal_places=8, null=True)
    price_1h = models.FloatField(max_length=24, default=0.00, null=True, blank=True)
    price_24h = models.FloatField(max_length=24, default=0.00, null=True, blank=True)
    price_btc = models.DecimalField(max_digits=16, decimal_places=8, null=True, blank=True)
    price_eth = models.DecimalField(max_digits=16, decimal_places=8, null=True, blank=True)

    def __str__(self):
        return self.symbol


class Coin(models.Model):
    objects = models.Manager()  # gets rid of linter (query) issues
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    date_bought = models.DateTimeField(default=datetime.utcnow)
    date_sold = models.DateTimeField(null=True, blank=True)
    sell_price = models.DecimalField(max_digits=16, decimal_places=8, null=True, blank=True)
    merged = models.BooleanField(default=False)
    sold = models.BooleanField(default=False)
    gain = models.DecimalField(max_digits=16, decimal_places=8, null=True, blank=True)
    amount = models.DecimalField(max_digits=16, decimal_places=8, default=0.00)
    total_amount = models.DecimalField(max_digits=16, decimal_places=8, default=0.00)
    value = models.DecimalField(max_digits=16, decimal_places=8, null=True, blank=True)
    total_value = models.DecimalField(max_digits=16, decimal_places=8, null=True, blank=True)
    total_spent = models.DecimalField(max_digits=16, decimal_places=8, null=True, blank=True)
    sell_amount = models.DecimalField(max_digits=16, decimal_places=8, null=True, default=0, blank=True)
    _purchase_price = models.DecimalField(max_digits=16, decimal_places=8, null=True, blank=True)
    custom_price = models.DecimalField(max_digits=16, decimal_places=8, default=0.00, null=True, blank=True)
    current_price = models.DecimalField(max_digits=16, decimal_places=8, default=0.00, blank=True)
    price_difference = models.FloatField(max_length=24, default=0.00, blank=True)
    total_profit = models.DecimalField(max_digits=16, decimal_places=8, null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def difference(self):
        return self.purchase_price - self.current_price

    @property
    def purchase_price(self):
        if not self._purchase_price:
            symbol = self.name[self.name.find('(') + 1:self.name.find(')')]
            api_url = 'https://data.messari.io/api/v1/assets/'+symbol.lower()+'/metrics'
            response = requests.get(api_url)
            data = response.json()
            try:
                self._purchase_price = decimal.Decimal(data['data']['market_data']['price_usd'])
            except KeyError:
                self._purchase_price = decimal.Decimal(0)
            self.current_price = self._purchase_price

        return self._purchase_price