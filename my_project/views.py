from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from my_project.forms import SignupForm


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            message = render_to_string('my_project/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            mail_subject = 'Activate account.'
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return render(request, 'base.html', {
                'alert': 'Please confirm your email address to complete the registration.',
                'title': "Home Page"
            })
    else:
        form = SignupForm()
    return render(request, 'my_project/signup.html', {
        'form': form,
        'title': "Register User"
    })


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return render(request, 'base.html', {
            'alert': 'Thank you for your email confirmation.',
            'title': "Home Page"
        })
    else:
        return render(request, 'base.html', {
            'alert': 'Activation link is invalid!',
            'title': "Home Page"
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
