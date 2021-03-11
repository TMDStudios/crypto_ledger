from django.shortcuts import render, redirect
# from django.views import generic
from django.views.generic import View
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from .forms import SignupForm

class UserRegisterView(View):
    form_class = SignupForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            form = self.form_class()
            return render(request, self.template_name, {'form': form, 
            'issue': 'User already exists.  Please choose a different username'})
