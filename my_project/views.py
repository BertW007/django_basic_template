import warnings
from django.contrib.auth import authenticate, login, REDIRECT_FIELD_NAME
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import deprecate_current_app, LoginView
from django.shortcuts import render, redirect


# Create your views here.
from django.utils.deprecation import RemovedInDjango21Warning


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'my_project/signup.html', {'form': form})
