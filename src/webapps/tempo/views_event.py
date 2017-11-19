from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from .models import *
from .forms import *


@login_required
def event(request):
    context = {}
    band = request.session['band']
    context['band_session'] = band
    context['band'] = Band.objects.get(id=band)
    if request.method == 'GET':
        context['form'] = EventForm()
        context['events'] = Event.objects.all()
        return render(request, 'events/eventmainpage.html', context)

#######################################################################################################

# def event(request, band_id):
#     context = {}
#     context['band'] = Band.objects.get(id=band_id)
#     if request.method == 'GET':
#         context['form'] = EventForm()
#         context['events'] = Event.objects.filter(band_name=band_id)
#         return render(request, 'events/eventmainpage.html', context)


#######################################################################################################
@login_required
def add_event(request, band_id):
    context = {}
    form = EventForm(request.POST)
    context['form'] = form
    errors = []
    context['errors'] = errors

    if not form.is_valid():
        return render(request, 'events/eventmainpage.html', context)

    else:
        band = Band.objects.get(id=band_id)
        new_event = Event(event_name=form.clean_event_name(), start_date=form.clean_start_date(),
                          end_date=form.clean_end_date(), event_type=form.clean_event_type(),
                          creator=request.user, band_name=band)
        new_event.save()

        return redirect(reverse('events'))

@login_required()
def get_events(request, band_id):
    band = Band.objects.get(id=band_id)
    events = Event.objects.filter(band_name=band)
    context = {"events": events}
    return render(request, 'events.json', context, content_type='application/json')
