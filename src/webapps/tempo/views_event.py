from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from . models import *
from . forms import *

@login_required
def event(request):
    context = {}
    if request.method == 'GET':
        context['form'] = EventForm()
        context['event'] = Event.objects.all()
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
        errors.append('Please provide list name')
        return render(request, 'songlist.html', context)

    else:
        new_item = Event(name=form.cleaned_data['name'])
        new_item.save()
        context['form'] = SongListForm()
        context['song_list'] = SongList.objects.all()

    return render(request, 'songlist.html', context)