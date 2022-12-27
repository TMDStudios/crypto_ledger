from django import forms
from .models import Coin, Profile

coin_names = [
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
        ('The Graph (GRT)', 'The Graph (GRT)'),
        ('Presearch (PRE)', 'Presearch (PRE)'),
        ('Aave (AAVE)', 'Aave (AAVE)'),
        ('Uniswap (UNI)', 'Uniswap (UNI)'),
        ('Phantasma (SOUL)', 'Phantasma (SOUL)'),
        ('NEO (NEO)', 'NEO (NEO)'),
        ('NEO GAS (GAS)', 'NEO GAS (GAS)'),
        ('Telcoin (TEL)', 'Telcoin (TEL)'),
        ('Maker (MKR)', 'Maker (MKR)'),
        ('Ren (REN)', 'Ren (REN)'),
        ('0x (ZRX)', '0x (ZRX)'),
        ('Decentraland (MANA)', 'Decentraland (MANA)'),
        ('Polygon (MATIC)', 'Polygon (MATIC)'),
        ('Binance Coin (BNB)', 'Binance Coin (BNB)'),
        ('Solana (SOL)', 'Solana (SOL)'),
        ('Shiba Inu (SHIB)', 'Shiba Inu (SHIB)'),
        ('USD Coin (USDC)', 'USD Coin (USDC)'),
        ('Terra (LUNA)', 'Terra (LUNA)'),
        ('Avalanche (AVAX)', 'Avalanche (AVAX)'),
        ('Wrapped Bitcoin (WBTC)', 'Wrapped Bitcoin (WBTC)'),
        ('Binance USD (BUSD)', 'Binance USD (BUSD)'),
        ('VeChain (VET)', 'VeChain (VET)'),
        ('Axie Infinity (AXS)', 'Axie Infinity (AXS)'),
    ]

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
        ('Telcoin (TEL)', 'TEL'),
        ('Cosmos (ATOM)', 'ATOM'),
        ('Augur (REP)', 'REP'),
        ('Basic Attention Token (BAT)', 'BAT'),
        ('The Graph (GRT)', 'GRT'),
        ('Kava (KAVA)', 'KAVA'),
        ('Chainlink (LINK)', 'LINK'),
        ('Uniswap (UNI)', 'UNI'),
        ('NEO GAS (GAS)', 'GAS'),
        ('Presearch (PRE)', 'PRE'),
        ('Phantasma (SOUL)', 'SOUL'),
        ('Aave (AAVE)', 'AAVE'),
        ('NEO (NEO)', 'NEO'),
        ('Ren (REN)', 'REN'),
        ('0x (ZRX)', 'ZRX'),
        ('Shiba Inu (SHIB)', 'SHIB'),
        ('Compound (COMP)', 'COMP'),
        ('Maker (MKR)', 'MKR'),
        ('Binance Coin (BNB)', 'BNB'),
        ('Solana (SOL)', 'SOL'),
        ('Terra (LUNA)', 'LUNA'),
        ('Decentraland (MANA)', 'MANA'),
        ('VeChain (VET)', 'VET'),
        ('Axie Infinity (AXS)', 'AXS'),
        ('Binance USD (BUSD)', 'BUSD'),
        ('Avalanche (AVAX)', 'AVAX'),
        ('USD Coin (USDC)', 'USDC'),
        ('Siacoin (SC)', 'SC'),
        ('Waves (WAVES)', 'WAVES'),
        ('Polygon (MATIC)', 'MATIC'),
        ('Storj (STORJ)', 'STORJ'),
        ('Wrapped Bitcoin (WBTC)', 'WBTC'),
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
            'name': forms.Select(choices=coin_names, attrs={'class': 'form-control'}),
            'amount': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'custom_price': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'placeholder': 'Leave Blank To Use Current Price'}),
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

class PaginationForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('transaction_view',)
        
        wwidgets = {
            'transaction_view': forms.NumberInput(attrs={
                'id': 'number_field',
                'style': 'width:5ch;', 
                'oninput': 'limit_input()',
                'step': 1
                }),
        }