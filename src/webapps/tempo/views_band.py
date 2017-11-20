from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse

from .models import *
from .forms import *

######################################################################################################
@login_required()
def band_page(request):
    context = {}
    context['user'] = request.user.username
    band = request.session['band']
    context['band_session'] = band
    context['band'] = Band.objects.get(id=band)
    context['user_bands'] = ArtistInBand.objects.filter(member=request.user)
    return render(request, 'bandpage.html', context)

######################################################################################################
def band_page(request):
    context['band_session'] = request.session['band']
    context['user_bands'] = ArtistInBand.objects.filter(member=request.user)
    return render(request, 'bandpage.html', context)


##########################################fuctions to join and create#############################################
# @login_required()
# def join(request):
#     context = {}
#     errors = []
#
#     form = BandForm(request.POST or None)
#
#     context['errors'] = errors
#     context['form'] = form
#     return render(request, 'band_join.html', context)

@login_required()
def create(request):
    context = {}
    errors = []

    form = BandForm(request.POST or None)
    context['errors'] = errors
    context['form'] = form
    return render(request, 'band_create.html', context)

@login_required()
def join_band(request, band_id):
    context = {}
    if Band.objects.filter(id=band_id):
        band_to_join = Band.objects.get(id=band_id)
        current_artist = request.user
        ArtistInBand.objects.create(band = band_to_join, member = current_artist)
        return redirect(reverse('user_pre_profile'))
    else:
        return redirect(reverse('user_pre_profile'))


@login_required()
def create_band(request):
    context = {}
    errors = []
    context['errors'] = errors

    # form = BandForm(request.POST or None)
    form = BandForm(request.POST, request.FILES)

    if not form.is_valid():
        errors = 'Something went wrong, try again.'
        context['errors'] = errors
        return render(request, 'band_create.html', context)

    band_name = form.cleaned_data['bandname']
    band_info = form.cleaned_data['band_info']
    city = form.cleaned_data['city']
    creator = request.user

    new_band = Band(band_name=band_name, band_info=band_info, city=city, creator=creator)
    if 'image' in request.FILES:
        new_band.image = request.FILES['image']

    new_band.save()

    request.session['band'] = new_band.id
    ArtistInBand.objects.create(band=new_band, member=request.user)

    context['current_artist'] = creator
    context['band'] = new_band
    context['message'] = 'created'

    return redirect(reverse('user_home', args={request.user.username}))


# fundtion to get list of available bands
@login_required()
def user_band_list(request):
    context = {}
    errors = []
    context['errors'] = errors

    current_artist = Artist.objects.get(artist=request.user.id)
    print("Current Artist" + str(current_artist.artist.username))
    # get list of bands he belongs to
    bands = Band.objects.filter(creator=current_artist.id)
    print("successfully " + str(bands))
    context['band'] = Band.objects.get(id=band_id)
    context['band_session'] = request.session['band']
    context['user_bands'] = ArtistInBand.objects.filter(member=request.user)
    return render(request, 'user_home.html', context)


# fundtion to get list of available bands
@login_required()
def band_list(request):
    context = {}
    context['all_bands'] = Band.objects.all()
    return render(request, 'user_pre_profile.html', context)

def team_member(request):
    context = {}
    band_id = request.session['band']
    artist_band_pair = ArtistInBand.objects.filter(band_id=band_id)
    context['band'] = Band.objects.get(id=band_id)
    context['team_member'] = User.objects.filter(band_member__in=artist_band_pair.values_list('member', flat=True)).distinct()
    #context['team_member'] = artist_band_pair
    print (str(artist_band_pair[0].member.id))
    context['band_name'] = Band.objects.get(id = band_id).band_name
    context['band_session'] = band_id
    context['user_bands'] = ArtistInBand.objects.filter(member=request.user)
    return render(request, 'team_member.html', context)