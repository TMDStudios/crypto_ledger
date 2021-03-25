from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add-coin/', views.add_coin, name='add-coin'),
    path('sell-coin/<int:id>', views.sell_coin, name='sell-coin'),
    path('delete-coin/<int:id>/', views.delete_coin, name='delete-coin'),
    path('coin-details/<int:id>/', views.coin_details, name='coin-details'),
    path('general-details/<int:id>/', views.general_details, name='general-details'),
    path('api/get-prices/', views.get_prices, name='get-prices'),
    path('api/get-user-ledger/', views.get_user_ledger, name='get-user-ledger'),
    path('all-prices/', views.all_prices, name='all-prices'),
    path('settings/', views.settings, name='settings'),
]