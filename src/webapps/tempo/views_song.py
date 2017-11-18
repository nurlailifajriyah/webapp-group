from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import *
from .forms import *
#######################################################################################################
@login_required
def song_list(request):
    context = {}
    if request.method == 'GET':
        band_id = request.session['band']
        band = Band.objects.filter(id=band_id)
        context['form'] = SongListForm()
        context['song_list'] = SongList.objects.filter(band=band)
        return render(request, 'songlist.html', context)


@login_required
def add_song_list(request):
    context = {}
    form = SongListForm(request.POST)
    band_id = request.session['band']
    band = Band.objects.get(id=band_id)
    context['form'] = form
    errors = []
    context['errors'] = errors

    if not form.is_valid():
        errors.append('Please provide list name')
        return render(request, 'songlist.html', context)

    else:
        new_item = SongList(name=form.cleaned_data['name'], band=band)
        new_item.save()
        context['form'] = SongListForm()
        context['song_list'] = SongList.objects.all()

    return render(request, 'songlist.html', context)

@login_required
def song(request):
    context = {}
    if request.method == 'GET':
        band_id = request.session['band']
        band = Band.objects.filter(id=band_id)
        context['form'] = SongForm()
        context['song_list'] = Song.objects.filter(band=band)
        return render(request, 'song.html', context)

@login_required
def add_song(request):
        context = {}
        form = SongForm(request.POST)
        band_id = request.session['band']
        band = Band.objects.get(id=band_id)
        context['form'] = form
        errors = []


        if not form.is_valid():
            errors.append('Please provide song information')
            context['errors'] = errors
            return render(request, 'song.html', context)

        else:
            new_item = Song.objects.create(name=form.cleaned_data['name'], band=band)
            if 'image' in request.FILES:
                new_item.image = request.FILES['image']
                new_item.save()
            if 'audio_file' in request.FILES:
                new_item.audio_file = request.FILES['audio_file']
                new_item.save()
            new_item.save()
            context['form'] = SongForm()
            context['song_list'] = Song.objects.filter(band=band)
        context['form'] = SongForm()
        context['song_list'] = Song.objects.filter(band=band)
        context['errors'] = errors
        return redirect(reverse('song'))

@login_required
def album(request):

    return render(request, 'album.html', {})