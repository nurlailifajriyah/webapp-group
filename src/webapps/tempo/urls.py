from django.conf.urls import include, url
from django.contrib.auth.views import login, logout_then_login
from django.contrib.auth import views as auth_views
from webapps import settings

import tempo.views
import tempo.views_audiorecording

urlpatterns = [
    url(r'^$', tempo.views.home, name="welcome"),
    url(r'^register', tempo.views.register, name='register'),
    url(r'^login$', login, {'template_name': 'login.html', 'redirect_authenticated_user': True}, name='login'),
    url(r'^logout$', logout_then_login),
    url(r'^personal_home', tempo.views.home, name='personal'),
    url(r'^user_pre_profile', tempo.views.user_pre_profile, name='user_pre_profile'),
    url(r'^user_home/(?P<username>\w+)$', tempo.views.user_home, name='user_home'),
    url(r'^band_page', tempo.views.band_page, name = 'band'),
    url(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',tempo.views.activate, name='activate'),
    url(r'^add_song_list$', tempo.views.add_song_list, name="add_song_list"),
    url(r'^song_list$', tempo.views.song_list, name="song_list"),
    url(r'^audio_recorder$', tempo.views_audiorecording.audio_recorder, name="audio_recorder"),
    url(r'^add_track$', tempo.views_audiorecording.add_track, name="add_track"),
    #url(r'^add_track(?P<track>\w+)$', tempo.views_audiorecording.add_track, name="add_track"),
    url(r'^get_track$', tempo.views_audiorecording.get_tracks, name="get_tracks"),
    url(r'^get_track/$', tempo.views_audiorecording.get_tracks, name="get_tracks"),
    url(r'^get_track/(?P<time>.+)$', tempo.views_audiorecording.get_tracks, name="get_tracks"),

]