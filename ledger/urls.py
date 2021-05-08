from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add-coin/', views.add_coin, name='add-coin'),
    path('sell-coin/<int:id>', views.sell_coin, name='sell-coin'),
    path('delete-coin/<int:id>/', views.delete_coin, name='delete-coin'),
    path('reset-ledger/', views.reset_ledger, name='reset-ledger'),
    path('coin-details/<int:id>/', views.coin_details, name='coin-details'),
    path('general-details/<int:id>/', views.general_details, name='general-details'),
    path('api/docs/', views.api_docs, name='api-docs'),
    path('api/get-prices/', views.get_prices, name='get-prices'),
    path('api/set-prices/', views.set_prices, name='set-prices'),
    path('api/get-user-ledger/<str:api_token>', views.GetUserLedger.as_view(), name='get-user-ledger'),
    path('api/buy-coin-api/<str:api_token>', views.BuyCoinAPI.as_view(), name='buy-coin-api'),
    path('api/sell-coin-api/<str:api_token>', views.SellCoinAPI.as_view(), name='sell-coin-api'),
    path('all-prices/', views.all_prices, name='all-prices'),
    path('settings/', views.settings, name='settings'),
]