from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import *
from .forms import *


@login_required
def event(request):
    context = {}
    if request.method == 'GET':
        context['form'] = EventForm()
        context['events'] = Event.objects.all()
        return render(request, 'events/eventmainpage.html', context)

#######################################################################################################

def event(request, band_id):
    context = {}
    context['band'] = Band.objects.get(id=band_id)
    if request.method == 'GET':
        context['form'] = EventForm()
        context['events'] = Event.objects.filter(band_name=band_id)
        return render(request, 'events/eventmainpage.html', context)


#######################################################################################################
@login_required
def add_event(request):
    context = {}
    form = EventForm(request.POST)
    context['form'] = form
    errors = []
    context['errors'] = errors

    if not form.is_valid():
        return render(request, 'events/eventmainpage.html', context)

    else:
        new_event = Event(name=form.cleaned_data['name'], creator=request.user)
        new_event.save()
        context['form'] = EventForm()
        context['event'] = Event.objects.all()

    return render(request, 'events/eventmainpage.html', context)
