from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse, Http404, JsonResponse
from . models import *
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

@login_required
def audio_recorder(request, song_id):
    context ={}
    song = get_object_or_404(Song, id=song_id)
    context['band_session'] = request.session['band']

    context['song'] = song
    return render(request, 'audio_record.html', context)

@login_required
def add_track(request):
    # TODO validation if file is not an audio file
    errors = []
    if not 'track_name' in request.POST or not request.POST['track_name']:
        errors.append('Trackname is required.')
    else:
        song = Song.objects.get(id=request.session['song_id'])
        new_track = Track(name=request.POST['track_name'], type="wave", audio_file=request.FILES['data'], version_number=1, song=song)
        new_track.save()
    return HttpResponse("")

@login_required
def get_tracks(request, time="1970-01-01T00:00+00:00"):
    max_time = Track.get_max_time()
    tracks = Track.get_tracks(time)
    context = {"max_time": max_time, "tracks": tracks}
    return render(request, 'tracks/tracks.json', context, content_type='application/json')