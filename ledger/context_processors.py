from .models import Profile, Price, Date
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from datetime import datetime

def extras(request):
    update_now = False
    if request.user.is_authenticated:
        owner = get_object_or_404(User, id=request.user.id)
        user_profile = Profile.objects.all().filter(user=owner)

        if not user_profile:
            user_profile = Profile(user=owner, ticker_prices="")
            user_profile.save()
        user_profile = Profile.objects.all().filter(user=owner)[0]

        dark_mode = user_profile.dark_mode
    else:
        dark_mode = True

    prices = Price.objects.all()
    prices = prices.order_by('name')

    bitcoin_price = prices.filter(symbol='BTC')[0].price

    try:
        saved_update = Date.objects.all()[0]
    except IndexError:
        saved_update = Date(last_update=datetime.utcnow())
        saved_update.update_round = 0
        saved_update.save()

    temp_time = datetime.strptime(str(datetime.utcnow().time()).split('.')[0], '%H:%M:%S')
    last_update = temp_time.second + temp_time.minute * 60 + temp_time.hour * 3600

    try:
        temp_saved_time = datetime.strptime(str(saved_update).split(' ')[1].split('+')[0], '%H:%M:%S')
    except ValueError:
        temp_saved_time = datetime.strptime(str(saved_update).split(' ')[1].split('.')[0], '%H:%M:%S')
    current_time = temp_saved_time.second + temp_saved_time.minute * 60 + temp_saved_time.hour * 3600

    update_timer = last_update - current_time
    if update_timer > 60 or update_timer < -60:
        update_round = saved_update.update_round
        if update_round > 2:
            saved_update.update_round = 0
        else:
            saved_update.update_round += 1
        saved_update.last_update = datetime.utcnow()
        saved_update.save()

        update_now = True

    group = (
        'btc,eth,bch,dai,dash,doge,ltc,xmr,nano,paxg,xrp,xlm,ada,atom,eos,eth,etc,dot',
        'btc,eth,ksm,lsk,icx,omg,xtz,trx,waves,rep,bal,comp,crv,gno,kava,knc,snx,oxt',
        'btc,eth,storj,bat,usdt,mln,grt,pre,aave,uni,zec,algo,link,fil,neo,gas,soul,ren',
        'btc,eth,tel,mkr,mina,matic,dot,sc,zrx',
        ''
    )

    if update_now:
        return{'dark_mode': dark_mode, 'bitcoin_price': bitcoin_price, 'last_update': last_update, 
        'saved_update': saved_update, 'current_time': current_time, 'update_now': '> Reload to update prices <', 
        'fetch': group[update_round]}
    else:
        return{'dark_mode': dark_mode, 'bitcoin_price': bitcoin_price, 'last_update': last_update, 
        'saved_update': saved_update, 'current_time': current_time, 'fetch': group[3]}