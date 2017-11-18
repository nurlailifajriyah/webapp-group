from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *

######################################################################################################
@login_required
def get_photo(request, id):
    user_prof = get_object_or_404(Artist, artist_id=id)
    # if user hasn't uploaded image, manually return 404 error
    if not user_prof.image:
        raise Http404
    # manually set the content type of photo
    content_type = guess_type(user_prof.image.name)
    # manually set content type of photo
    return HttpResponse(user_prof.image, content_type=content_type)


######################################################################################################

@login_required
def get_band_photo(request, band_id):
    band_prof = get_object_or_404(Band, id=band_id)
    # if user hasn't uploaded image, manually return 404 error
    if not band_prof.image:
        raise Http404
    # manually set the content type of photo
    content_type = guess_type(band_prof.image.name)
    # manually set content type of photo
    return HttpResponse(band_prof.image, content_type=content_type)


@login_required
def get_song_photo(request, song_id):
    song_prof = get_object_or_404(Song, id=song_id)
    # if user hasn't uploaded image, manually return 404 error
    if not song_prof.image:
        raise Http404
    # manually set the content type of photo
    content_type = guess_type(song_prof.image.name)
    # manually set content type of photo
    return HttpResponse(song_prof.image, content_type=content_type)