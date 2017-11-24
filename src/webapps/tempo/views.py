# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import login
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string

from .models import *
from .forms import *
from django.core.urlresolvers import reverse
from django.http import HttpResponse, Http404, JsonResponse
from django.core.mail import send_mail
from mimetypes import guess_type
from .token import account_activation_token
from tempo.models import *
import json


# Homepage
def home(request):
    return render(request, 'welcome.html')


###############################################################################
@login_required
def user_pre_profile(request):
    context = {}
    # If the user have bands, they will be redirected to one of their band homepage
    if (ArtistInBand.objects.filter(member_id=request.user.id)):
        artist_band = ArtistInBand.objects.filter(member_id=request.user.id).first()
        request.session['band'] = artist_band.band.id
        return redirect(reverse('user_home', args={request.user.username}))
    # Else, they will go to user_pre_profile to join band first
    context['all_bands'] = Band.objects.all()
    return render(request, 'user_pre_profile.html', context)


#################################################################################
def register(request):
    if request.method == 'GET':
        context = {'form': RegistrationForm()}
        return render(request, 'register.html', context)

    form = RegistrationForm(request.POST)
    context = {'form': form}
    if not form.is_valid():
        return render(request, 'register.html', context)
    new_user = User.objects.create_user(username=form.cleaned_data['username'],
                                        first_name=form.cleaned_data['first_name'],
                                        last_name=form.cleaned_data['last_name'],
                                        email=form.cleaned_data['email'],
                                        password=form.cleaned_data['password1'],
                                        is_active=False
                                        )
    new_user.save()

    # profile part
    artist = Artist(age=form.cleaned_data['age'], artist=new_user, city=form.cleaned_data['city'],
                    country=form.cleaned_data['country'], bio=form.cleaned_data['bio'],
                    zipcode=form.cleaned_data['zipcode'])
    artist.save()

    # email part
    token = account_activation_token.make_token(new_user)
    email_body = """Welcome to Tempo. We are glad you became a member. Please verify your email address and explore the wonders:
    http://%s%s""" % (request.get_host(),
                      reverse('activate', args=(new_user.username, token)))

    send_mail(subject="Verify your account/email address",
              message=email_body,
              from_email="grumbltech@grumblr.com",
              recipient_list=[new_user.email])
    context['email'] = form.cleaned_data['email']
    context['fname'] = form.cleaned_data['first_name']
    return render(request, "acc_active_email.html", context)


####################################LOGIN######################################################
def activate(request, uidb64, token):
    try:
        user = User.objects.get(username=uidb64)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    # check if user exists in database (inactive) and verify their token by calling token.py and set user to active
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return render(request,'Post_Verification.html')
        return HttpResponse(
            'Thank you for your email confirmation. Now you can login your account.' + '<a href = "/#middle"><p>Log in</p></a>')
    else:
        return HttpResponse('Activation link is invalid!')


#######################################################################################################
@login_required
def user_home(request, username):
    try:
        context = {}
        # user_bands to show all bands the user joined in the header_base
        context['user_bands'] = ArtistInBand.objects.filter(member=request.user)
        # get band id from session
        band_id = request.session['band']
        band = Band.objects.filter(id=band_id)
        context['username'] = username
        context['band'] = Band.objects.get(id=band)
        context['song_list'] = SongList.objects.filter(band=band)
        artist_band_pair = ArtistInBand.objects.filter(band_id=band_id)
        context['team_member'] = User.objects.filter(band_member__in=artist_band_pair.values_list('member', flat=True)).distinct()
        return render(request, 'user_home.html', context)
    except ObjectDoesNotExist as e:
        return render(request, 'welcome.html', {})


###################################################################################################
@login_required
def change_band_home(request, band_id):
    try:
        context = {}
        context['user_bands'] = ArtistInBand.objects.filter(member=request.user)
        context['band'] = Band.objects.get(id=band_id)
        request.session['band'] = band_id
        return redirect(reverse('user_home', args={request.user.username}))
    except ObjectDoesNotExist as e:
        return redirect(reverse('user_home', args={request.user.username}))





