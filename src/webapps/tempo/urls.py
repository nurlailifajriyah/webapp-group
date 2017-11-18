from django.conf.urls import include, url
from django.contrib.auth.views import login, logout_then_login
from django.contrib.auth import views as auth_views
from webapps import settings

import tempo.views
import tempo.views_event
import tempo.views_audiorecording

urlpatterns = [

    url(r'^$', tempo.views.home, name="welcome"),
    url(r'^register$', tempo.views.register, name='register'),
    url(r'^login$', login, {'template_name': 'login.html', 'redirect_authenticated_user': True}, name='login'),
    url(r'^logout$', logout_then_login),
    #url(r'^personal_home', tempo.views.home, name='personal'),
    url(r'^user_pre_profile', tempo.views.user_pre_profile, name='user_pre_profile'),

    url(r'^user_home/(?P<username>\w+)$', tempo.views.user_home, name='user_home'),

    url(r'^calendar$', tempo.views.calendar, name = 'calendar'),
    url(r'^calendar/(?P<band_id>\d+)$', tempo.views.band_calendar, name = 'calendar'),

    url(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',tempo.views.activate, name='activate'),

    # Songlist
    url(r'^add_song_list$', tempo.views.add_song_list, name="add_song_list"),
    url(r'^song_list$', tempo.views.song_list, name="song_list"),
    url(r'^song$', tempo.views.song, name="song"),
    url(r'^add_song$', tempo.views.add_song, name="add_song"),

    # Tracks
    url(r'^audio_recorder$', tempo.views_audiorecording.audio_recorder, name="audio_recorder"),
    url(r'^add_track$', tempo.views_audiorecording.add_track, name="add_track"),
    url(r'^get_track$', tempo.views_audiorecording.get_tracks, name="get_tracks"),
    url(r'^get_track/$', tempo.views_audiorecording.get_tracks, name="get_tracks"),
    url(r'^get_track/(?P<time>.+)$', tempo.views_audiorecording.get_tracks, name="get_tracks"),

    # Events
    url(r'^events$', tempo.views_event.event, name='events'),
    url(r'^events/(?P<band_id>\d+)$', tempo.views_event.event, name='bandevents'),
    url(r'^add_event/(?P<band_id>\d+)$', tempo.views_event.add_event, name='add_event'),
    url(r'^get_events/(?P<band_id>\d+)$', tempo.views_event.get_events, name='getbandevents'),

    #band
    url(r'^band_page', tempo.views.band_page, name='band'),
    url(r'^join_band/(?P<band_id>\d+)$', tempo.views.join_band, name='join_band'),
    url(r'^create_band$', tempo.views.create_band, name='create_band'),
    url(r'^user_band_list$', tempo.views.user_band_list, name='user_band_list'),
    url(r'^band_list$', tempo.views.band_list, name='band_list'),
    #url(r'^band_events/(?P<band_id>\d+)$', tempo.views.band_events, name='band_events'),
    url(r'^team_members$', tempo.views.team_member, name='team_members'),

    #url(r'^join$', tempo.views.join, name='join'),
    url(r'^create$', tempo.views.create, name='create'),


    # url(r'^confirm/', include('generic_confirmation.urls')),

    url(r'^photo/(?P<id>\d+)$', tempo.views.get_photo, name='photo'),
    url(r'^band_photo/(?P<band_id>\d+)$', tempo.views.get_band_photo, name='band_photo'),
    url(r'^edit_profile/(?P<username>\w+)$', tempo.views.edit_profile, name='edit_profile'),

]