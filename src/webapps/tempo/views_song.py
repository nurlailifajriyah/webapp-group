from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
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
        context['band_session'] = band_id
        return render(request, 'songlist.html', context)

@login_required
def song_detail(request,song_id):

    context = {}
    valid_song = get_object_or_404(Song, id=song_id)
    if request.method == 'GET':
        band_id = request.session['band']
        band = Band.objects.filter(id=band_id)
        context['band'] = band
        context['song'] = valid_song
        request.session['song_id'] = valid_song.id
        context['band_session'] = band_id
        return render(request, 'song_detail.html', context)


@login_required
def add_song_list(request):
    context = {}
    form = SongListForm(request.POST)
    band_id = request.session['band']
    band = Band.objects.get(id=band_id)
    context['form'] = form
    errors = []
    context['errors'] = errors
    context['band_session'] = band_id

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
        context['band_session'] = band_id
        band = Band.objects.filter(id=band_id)
        context['form'] = SongForm()
        context['song_list'] = Song.objects.filter(band=band)
        return render(request, 'song.html', context)

@login_required
def add_song(request):
        context = {}
        form = SongForm(request.POST)
        band_id = request.session['band']
        context['band_session'] = band_id
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
    context = {}
    context['band_session'] = request.session['band']
    return render(request, 'album.html', context)