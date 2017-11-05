# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import login
from django.contrib.auth.decorators import login_required
from . models import *
from .  forms import *
from django.core.urlresolvers import reverse
from django.http import HttpResponse, Http404, JsonResponse
from django.core.mail import send_mail
from mimetypes import guess_type
from .token import account_activation_token
from tempo.models import *


# Create your views here.
def home(request):
    return render(request, 'welcome.html')

###############################################################################
def user_pre_profile(request):
    context = {'user': request.user, 'details': request.user.username}
    return render(request, 'user_pre_profile.html', context)
#################################################################################
def register(request):
    if request.method == 'GET':
        context = {'form':RegistrationForm()}
        return render(request, 'register.html', context)

    form = RegistrationForm(request.POST)
    context = {'form': form}
    if not form.is_valid():
        return render(request, 'register.html', context)
    new_user = User.objects.create_user(username = form.cleaned_data['username'],
                                          first_name = form.cleaned_data['first_name'],
                                          last_name = form.cleaned_data['last_name'],
                                          email=form.cleaned_data['email'],
                                          password= form.cleaned_data['password1'],
                                          is_active = False
                                          )
    new_user.save()

    #profile part
    artist = Artist(age=form.cleaned_data['age'], artist=new_user, city=form.cleaned_data['city'],
                    country=form.cleaned_data['country'], bio=form.cleaned_data['bio'],zipcode=form.cleaned_data['zipcode'])
    # artist.image = 'tempo/media/12522937_1257065594310510_6977590312724746127_n.jpg'
    artist.save()

    # return render(request, 'register.html', context)

    # ### email part
    token = account_activation_token.make_token(new_user)
    email_body = """Welcome to Tempo. We are glad you became a member. Please verify your email address and explore the wonders:
    http://%s%s""" %(request.get_host(),
                     reverse('activate', args=(new_user.username, token)))
    #
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
    #check if user exists in database (inactive) and verify their token by calling token.py and set user to active
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        #return render(request,'Post_Verification.html')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')

#################################################################################################
@login_required
def profile(request, username):
    context = {}
    login_user = request.user
    try:
        userobj = User.objects.get(username=username)
        user_profile = userobj.profile
        #get the list of all followers for users
        follower_list = login_user.profile.follow.all()
        only_id_list = []
        for z in follower_list:
            only_id_list.append(z.user.id)
        id = userobj.id
        ##########################################################
        form = CommentForm(request.POST or None)
        if 'post' in request.POST and request.method != 'GET':
            context = add_posts(request,userobj,username)
            all_posts = context['user_posts']
            context['id'] = userobj.id
            context['profile'] = user_profile
            context['follow_list'] = only_id_list
            context['form'] = form


            ######################################################
            post_comm = []
            for k in all_posts:
                comm = Comment.objects.filter(post=k).order_by('-ctime')
                post_comm.append(comm)
                #here part cut
            context['post_comm'] = post_comm
            #######################################################
            return render(request, 'Profile.html', context)

        else:
            all_posts = User_Post.objects.filter(user=userobj).order_by('-time')
            ############################################################################
            # post_comm = {}
            post_comm = []
            for k in all_posts:
                comm = Comment.objects.filter(post=k).order_by('-ctime')
                post_comm.append(comm)
                #here part 2 cut
            context = {'post_comm': post_comm,'user_posts': all_posts, 'details': username, 'id':id, 'profile':user_profile, 'follow_list':only_id_list,'log_user_page':userobj, 'form':form}
            ###############################################################################

            return render(request, 'Profile.html',context)
    except ObjectDoesNotExist as e:
        #if the user doesn't exist in the database, it redirects to the global stream page
        return redirect(reverse('global'))
#######################################################################################################
@login_required
def user_home(request, username):
    context = {}
    try:
        login_user = request.user
        artistobj = User.objects.get(username=username)
        profile = artistobj.artist
        context = {'details':username, 'profile': profile, 'user': artistobj}
        return render(request, 'user_home.html',context)
    except ObjectDoesNotExist as e:
        return render(request, 'welcome.html', {})

######################################################################################################
def band_page(request):
    return render(request, 'bandpage.html', {})
#######################################################################################################
@login_required
def song_list(request):
    context = {}
    if request.method == 'GET':
        context['form'] = SongListForm()
        context['song_list'] = SongList.objects.all()
        return render(request, 'songlist.html', context)

#######################################################################################################
@login_required
def add_song_list(request):
    context = {}
    form = SongListForm(request.POST)
    context['form'] = form

    if not form.is_valid():
        return render(request, 'songlist.html', context)

    else:
        login_user = request.user
        new_item = SongList(name=form.cleaned_data['name'], user = login_user)
        new_item.save()
    return HttpResponse("")