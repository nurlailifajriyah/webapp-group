from django.conf.urls import include, url
from django.contrib.auth.views import login, logout_then_login

import tempo.views


urlpatterns = [
    url(r'^$', tempo.views.home),
    ]