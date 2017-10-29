from django.conf.urls import include, url
from django.contrib.auth.views import login, logout_then_login
from django.contrib.auth import views as auth_views
from webapps import settings

import tempo.views


urlpatterns = [
    url(r'^$', tempo.views.home),
    url(r'^login$', login, {'template_name': 'login.html', 'redirect_authenticated_user': True}, name='login'),

    ]