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
        context['band'] = Band.objects.get(id=band_id)
        context['user_bands'] = ArtistInBand.objects.filter(member=request.user)
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
        context['band'] = Band.objects.get(id=band_id)
        context['user_bands'] = ArtistInBand.objects.filter(member=request.user)
        return render(request, 'song_detail.html', context)

@login_required
def album_detail(request,album_id):

    context = {}
    album = get_object_or_404(SongList, id=album_id)
    if request.method == 'GET':
        song_in_album = SongInList.objects.filter(list=album)
        context['song'] = Song.objects.filter(id__in=song_in_album.values_list('song', flat=True))
        print (song_in_album.values_list('song', flat=True) )
        context['album_id'] = album_id
        band_id = request.session['band']
        band = Band.objects.filter(id=band_id)
        context['all_song_list'] = Song.objects.filter(band=band)
        context['band'] = band
        context['user_bands'] = ArtistInBand.objects.filter(member=request.user)
        return render(request, 'album_detail.html', context)

@login_required
def add_song_to_list(request,album_id):
    valid_song_list = get_object_or_404(SongList, id=album_id)
    if request.POST['checked_song']:
        for i in request.POST.getlist('checked_song'):
            print (i)
            song = Song.objects.get(id=i)
            new_item = SongInList(list=valid_song_list, song=song)
            new_item.save()

    return redirect(reverse('album_detail', args={album_id}))



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
    context['band'] = Band.objects.get(id=band_id)
    context['user_bands'] = ArtistInBand.objects.filter(member=request.user)

    if not form.is_valid():
        errors.append('Please provide list name')
        return render(request, 'songlist.html', context)

    else:
        new_item = SongList(name=form.cleaned_data['name'], band=band)
        new_item.save()
        context['form'] = SongListForm()
        context['song_list'] = SongList.objects.all()

        return redirect(reverse('song_list'))

@login_required
def song(request):
    context = {}
    if request.method == 'GET':
        band_id = request.session['band']
        context['band_session'] = band_id
        band = Band.objects.filter(id=band_id)
        context['form'] = SongForm()
        context['song_list'] = Song.objects.filter(band=band)
        context['band'] = Band.objects.get(id=band_id)
        context['user_bands'] = ArtistInBand.objects.filter(member=request.user)
        return render(request, 'song.html', context)

@login_required
def add_song(request):
        context = {}
        form = SongForm(request.POST)
        band_id = request.session['band']
        context['band_session'] = band_id
        band = Band.objects.get(id=band_id)
        context['form'] = form
        context['band'] = band
        context['user_bands'] = ArtistInBand.objects.filter(member=request.user)
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
    band_id = request.session['band']
    context['band_session'] = band_id
    context['band'] = Band.objects.get(id=band_id)
    context['user_bands'] = ArtistInBand.objects.filter(member=request.user)
    return render(request, 'album.html', context)