from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse, Http404, JsonResponse
from . models import *
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import login
from django.contrib.auth.decorators import login_required

@login_required
def audio_recorder(request):
    return render(request, 'audio_record.html', {})

@login_required
def add_track(request):
    # TODO validation if file is not an audio file
    new_track = Track(name="track.wav", type="wave", audio_file=request.FILES['data'], version_number=1)
    new_track.save()
    return HttpResponse("")

@login_required
def get_tracks(request, time="1970-01-01T00:00+00:00"):
    max_time = Track.get_max_time()
    tracks = Track.get_tracks(time)
    context = {"max_time": max_time, "tracks": tracks}
    return render(request, 'tracks/tracks.json', context, content_type='application/json')