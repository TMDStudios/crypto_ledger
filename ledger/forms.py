from django import forms
from .models import Coin, Profile

coins = [
        ('Bitcoin (BTC)', 'Bitcoin (BTC)'),
        ('Bitcoin Cash (BCH)', 'Bitcoin Cash (BCH)'),
        ('Dai (DAI)', 'Dai (DAI)'),
        ('Dash (DASH)', 'Dash (DASH)'),
        ('Dogecoin (DOGE)', 'Dogecoin (DOGE)'),
        ('Litecoin (LTC)', 'Litecoin (LTC)'),
        ('Monero (XMR)', 'Monero (XMR)'),
        ('Nano (NANO)', 'Nano (NANO)'),
        ('Paxos Gold (PAXG)', 'Paxos Gold (PAXG)'),
        ('Ripple (XRP)', 'Ripple (XRP)'),
        ('Stellar (XLM)', 'Stellar (XLM)'),
        ('Tether (USDT)', 'Tether (USDT)'),
        ('Zcash (ZEC)', 'Zcash (ZEC)'),
        ('Algorand (ALGO)', 'Algorand (ALGO)'),
        ('Cardano (ADA)', 'Cardano (ADA)'),
        ('Cosmos (ATOM)', 'Cosmos (ATOM)'),
        ('EOSIO (EOS)', 'EOSIO (EOS)'),
        ('Ethereum (ETH)', 'Ethereum (ETH)'),
        ('Ethereum Classic (ETC)', 'Ethereum Classic (ETC)'),
        ('Icon (ICX)', 'Icon (ICX)'),
        ('Kusama (KSM)', 'Kusama (KSM)'),
        ('Lisk (LSK)', 'Lisk (LSK)'),
        ('OmiseGo (OMG)', 'OmiseGo (OMG)'),
        ('Polkadot (DOT)', 'Polkadot (DOT)'),
        ('Tezos (XTZ)', 'Tezos (XTZ)'),
        ('Tron (TRX)', 'Tron (TRX)'),
        ('Waves (WAVES)', 'Waves (WAVES)'),
        ('Augur (REP)', 'Augur (REP)'),
        ('Balancer (BAL)', 'Balancer (BAL)'),
        ('Compound (COMP)', 'Compound (COMP)'),
        ('Curve (CRV)', 'Curve (CRV)'),
        ('Gnosis (GNO)', 'Gnosis (GNO)'),
        ('Kava (KAVA)', 'Kava (KAVA)'),
        ('Kyber Network (KNC)', 'Kyber Network (KNC)'),
        ('Melon (MLN)', 'Melon (MLN)'),
        ('Syntetix (SNX)', 'Syntetix (SNX)'),
        ('Chainlink (LINK)', 'Chainlink (LINK)'),
        ('Filecoin (FIL)', 'Filecoin (FIL)'),
        ('Orchid (OXT)', 'Orchid (OXT)'),
        ('Siacoin (SC)', 'Siacoin (SC)'),
        ('Storj (STORJ)', 'Storj (STORJ)'),
        ('Basic Attention Token (BAT)', 'Basic Attention Token (BAT)'),
    ]


class SettingsForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('ticker_prices', 'dark_mode')
        
        widgets = {
            'ticker_prices': forms.CheckboxSelectMultiple(choices=coins),
            'dark_mode': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'style': 'width: 5vw; height: 24px;'
                })
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
