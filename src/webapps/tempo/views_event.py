from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from .models import *
from .forms import *


@login_required
def event(request):
    context = {}
    band_session = request.session['band']
    context['band_session'] = band_session
    band = Band.objects.get(id=band_session)
    context['band'] = band
    context['user_bands'] = ArtistInBand.objects.filter(member=request.user)
    if request.method == 'GET':
        context['form'] = EventForm(band_id=band_session)
        context['events'] = Event.objects.filter(band_name=band)
        return render(request, 'events/eventmainpage.html', context)

@login_required
def add_event(request, band_id):
    valid_band = get_object_or_404(Band, id=band_id)
    context = {}
    form = EventForm(request.POST,band_id=band_id)
    context['form'] = form
    band_session = request.session['band']
    context['band_session'] = band_session
    band = Band.objects.get(id=band_session)
    context['band'] = band
    context['user_bands'] = ArtistInBand.objects.filter(member=request.user)

    if not form.is_valid():
        context['band'] = Band.objects.get(id=band_id)
        context['errors'] = form.errors
        context['events'] = Event.objects.filter(band_name=band)
        return render(request, 'events/eventmainpage.html', context)

    else:
        band = Band.objects.get(id=band_id)
        new_event = Event(event_name=form.clean_event_name(), start_date=form.clean_start_date(),
                          end_date=form.clean_end_date(), event_type=form.clean_event_type(),
                          creator=request.user, band_name=band)
        if form.data['song_list']:
            song_list = SongList.objects.get(id=form.data['song_list'])
            new_event.list = song_list
        form.clean()
        new_event.save()
        return redirect(reverse('events'))

@login_required()
def get_events(request, band_id):
    valid_band = get_object_or_404(Band, id=band_id)
    band = Band.objects.get(id=band_id)
    events = Event.objects.filter(band_name=band)
    context = {"events": events}
    return render(request, 'events.json', context, content_type='application/json')
