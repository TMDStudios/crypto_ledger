from .models import Profile
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

def extras(request):
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

    return{'dark_mode': dark_mode}