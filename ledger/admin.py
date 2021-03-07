from django.contrib import admin
from .models import Coin, Price, Date, Profile

admin.site.register(Coin)
admin.site.register(Price)
admin.site.register(Date)
admin.site.register(Profile)
