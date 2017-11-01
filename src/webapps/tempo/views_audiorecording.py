from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse, Http404, JsonResponse
from . models import *

def audio_recorder(request):
    return render(request, 'audio_record.html', {})

def add_track(request):
    new_track = Track(name="track.wav", type="wave", audio_file=request.FILES['data'], version_number=1)
    # new_track = Track(name="track.wav", type="wave", version_number=1)
    new_track.save()
    return HttpResponse("")