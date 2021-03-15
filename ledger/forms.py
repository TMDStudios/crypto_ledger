from django import forms
from .models import Coin, Profile

coins = [
        ('Bitcoin (BTC)', 'BTC'),
        ('Bitcoin Cash (BCH)', 'BCH'),
        ('Dai (DAI)', 'DAI'),
        ('Monero (XMR)', 'XMR'),
        ('Dash (DASH)', 'DASH'),
        ('Zcash (ZEC)', 'ZEC'),
        ('Stellar (XLM)', 'XLM'),
        ('Litecoin (LTC)', 'LTC'),
        ('Ripple (XRP)', 'XRP'),
        ('Dogecoin (DOGE)', 'DOGE'),
        ('Cardano (ADA)', 'ADA'),
        ('EOSIO (EOS)', 'EOS'),
        ('Ethereum (ETH)', 'ETH'),
        ('Ethereum Classic (ETC)', 'ETC'),
        ('Nano (NANO)', 'NANO'),
        ('Icon (ICX)', 'ICX'),
        ('Kusama (KSM)', 'KSM'),
        ('Lisk (LSK)', 'LSK'),
        ('OmiseGo (OMG)', 'OMG'),
        ('Paxos Gold (PAXG)', 'PAXG'),
        ('Polkadot (DOT)', 'DOT'),
        ('Tezos (XTZ)', 'XTZ'),
        ('Tron (TRX)', 'TRX'),
        ('Balancer (BAL)', 'BAL'),
        ('Tether (USDT)', 'USDT'),
        ('Curve (CRV)', 'CRV'),
        ('Gnosis (GNO)', 'GNO'),
        ('Kyber Network (KNC)', 'KNC'),
        ('Melon (MLN)', 'MLN'),
        ('Algorand (ALGO)', 'ALGO'),
        ('Syntetix (SNX)', 'SNX'),
        ('Filecoin (FIL)', 'FIL'),
        ('Orchid (OXT)', 'OXT'),
        ('Compound (COMP)', 'COMP'),
        ('Cosmos (ATOM)', 'ATOM'),
        ('Augur (REP)', 'REP'),
        ('Basic Attention Token (BAT)', 'BAT'),
        ('Siacoin (SC)', 'SC'),
        ('Kava (KAVA)', 'KAVA'),
        ('Chainlink (LINK)', 'LINK'),
        ('Waves (WAVES)', 'WAVES'),
        ('Storj (STORJ)', 'STORJ'),
    ]


class SettingsForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('ticker_prices', 'dark_mode', 'limit_history')
        
        widgets = {
            'ticker_prices': forms.CheckboxSelectMultiple(choices=coins),
            'dark_mode': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'style': 'width: 96px; height: 24px;'
                }),
            'limit_history': forms.NumberInput(attrs={'class': 'form-control'})
        }


class CoinForm(forms.ModelForm):
    class Meta:
        model = Coin
        fields = ('name', 'amount', 'custom_price')
        
        widgets = {
            'name': forms.Select(choices=coins, attrs={'class': 'form-control'}),
            'amount': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'custom_price': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'placeholder': 'Leave Blank To Use Current Price'}),
        }


class EditCoinForm(forms.ModelForm):
    class Meta:
        model = Coin
        fields = ('date_bought', 'date_sold', 'amount', 'total_amount', 'gain', '_purchase_price', 'sold')
        
        widgets = {
            'date_bought': forms.DateInput(format='%d/%m/%Y', attrs={'class': 'form-control'}),
            'date_sold': forms.DateInput(format='%d/%m/%Y', attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': 0.00000001}),
            'total_amount': forms.NumberInput(attrs={'class': 'form-control', 'step': 0.00000001}),
            'gain': forms.NumberInput(attrs={'class': 'form-control', 'step': 0.00000001}),
            '_purchase_price': forms.NumberInput(attrs={'class': 'form-control', 'step': 0.00000001}),
        }


class SellForm(forms.ModelForm):
    class Meta:
        model = Coin
        fields = ('sell_amount',)
        
        widgets = {
            'sell_amount': forms.NumberInput(attrs={
                'id': 'number_field',
                'style': 'width:12ch;', 
                'oninput': 'limit_input()',
                'step': 0.00000001
                }),
        }
