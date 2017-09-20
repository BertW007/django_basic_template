"""django_basic_template URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from my_project import views

urlpatterns = [
    url(r'^admin/',
        admin.site.urls),
    url(r'^signup/$',
        views.signup, name='signup'),
    url(r'^login/$',
        auth_views.login,  {'template_name': 'my_project/login.html'}, name='login'),
    url(r'^logout/$',
        auth_views.logout, name='logout'),
    url(r'^$',
        views.home, name='home'),
    url(r'^password/$',
        views.change_password, name='change_password'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    url(r'^password_reset/$',
        auth_views.password_reset, {'template_name': 'my_project/password_reset_form.html'}, name='password_reset'),
    url(r'^password_reset/done/$',
        auth_views.password_reset_done, {'template_name': 'my_project/password_reset_done.html'},
        name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, {'template_name': 'my_project/password_reset_confirm.html'},
        name='password_reset_confirm'),
    url(r'^reset/done/$',
        auth_views.password_reset_complete, {'template_name': 'my_project/password_reset_complete.html'},
        name='password_reset_complete'),
    url(r'^update_user/',
        views.UserUpdateView.as_view(), name='update'),
    url(r'^delete_user/',
        views.UserDeleteView.as_view(), name='delete'),
]
