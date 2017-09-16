from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.shortcuts import render, redirect


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
    return render(request, 'my_project/signup.html', {
        'form': form,
        'title': "Register User"
    })


def home(request):
    return render(request, 'base.html', {
        'title': "Home Page",
    })


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return render(request, 'base.html', {
                'title': "Home Page",
                'alert': ":-)"
            })
        else:
            return render(request, 'my_project/change_password.html', {
                'title': "Change Password",
                'alert': "ERROR"
            })
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'my_project/change_password.html', {
        'form': form,
        'title': "Change Password"
    })
