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


# Create your views here.
def home(request):
    return render(request, 'welcome.html')


###############################################################################
@login_required
def user_pre_profile(request):
    context = {}
    if (ArtistInBand.objects.filter(member_id=request.user.id)):
        return redirect(reverse('user_home', args={request.user.username}))

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
    # artist.image = 'tempo/media/12522937_1257065594310510_6977590312724746127_n.jpg'
    artist.save()

    # return render(request, 'register.html', context)

    # ### email part
    token = account_activation_token.make_token(new_user)
    email_body = """Welcome to Tempo. We are glad you became a member. Please verify your email address and explore the wonders:
    http://%s%s""" % (request.get_host(),
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
    # check if user exists in database (inactive) and verify their token by calling token.py and set user to active
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return render(request,'Post_Verification.html')
        return HttpResponse(
            'Thank you for your email confirmation. Now you can login your account.' + '<a href = "/login"><p>Login</p></a>')
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
        # get the list of all followers for users
        follower_list = login_user.profile.follow.all()
        only_id_list = []
        for z in follower_list:
            only_id_list.append(z.user.id)
        id = userobj.id
        ##########################################################
        form = CommentForm(request.POST or None)
        if 'post' in request.POST and request.method != 'GET':
            context = add_posts(request, userobj, username)
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
                # here part cut
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
                # here part 2 cut
            context = {'post_comm': post_comm, 'user_posts': all_posts, 'details': username, 'id': id,
                       'profile': user_profile, 'follow_list': only_id_list, 'log_user_page': userobj, 'form': form}
            ###############################################################################

            return render(request, 'Profile.html', context)
    except ObjectDoesNotExist as e:
        # if the user doesn't exist in the database, it redirects to the global stream page
        return redirect(reverse('global'))


#######################################################################################################
@login_required
def user_home(request, username):
    context = {}
    try:
        login_user = request.user
        artistobj = User.objects.get(username=username)
        profile = artistobj.artist
        context = {'details': username, 'profile': profile, 'user': artistobj}
        return render(request, 'user_home.html', context)
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
    errors = []
    context['errors'] = errors

    if not form.is_valid():
        errors.append('Please provide list name')
        return render(request, 'songlist.html', context)

    else:
        new_item = SongList(name=form.cleaned_data['name'])
        new_item.save()
        context['form'] = SongListForm()
        context['song_list'] = SongList.objects.all()

    return render(request, 'songlist.html', context)


###############################################################################

#################################################################################################
@login_required
# @transaction.commit_on_success
def edit_profile(request, username):
    try:
        user_to_edit = get_object_or_404(User, username=request.user.username)
        id = user_to_edit.id
        user_profile = user_to_edit.artist
        if request.method == 'GET':
            if username == request.user.username:
                # populate entries with the existing data in database and used related_name in model for onetoonefield
                form = ProfileEditForm(
                    initial={'first_name': user_to_edit.first_name, 'last_name': user_to_edit.last_name,
                             'email': user_to_edit.email, 'password_new1': user_to_edit.password,
                             'password_new2': user_to_edit.password, 'city': user_to_edit.artist.city,
                             'bio': user_to_edit.artist.bio,
                             'country': user_to_edit.artist.country, 'age': user_to_edit.artist.age})
                context = {'form': form, 'id': id}
                return render(request, 'edit.html', context)
            else:
                return redirect(reverse('edit_profile', args={request.user.username}))

        # if it is POST method, get FORM data to update the model
        form = ProfileEditForm(request.POST, request.FILES,
                               initial={'first_name': user_to_edit.first_name, 'last_name': user_to_edit.last_name,
                                        'email': user_to_edit.email, 'password_new1': user_to_edit.password,
                                        'password_new2': user_to_edit.password,
                                        'city': user_to_edit.artist.city, 'bio': user_to_edit.artist.bio,
                                        'country': user_to_edit.artist.country, 'age': user_to_edit.artist.age})
        context = {'form': form, 'id': id}

        if not form.is_valid():
            return render(request, 'edit.html', context)

        print(type(form.cleaned_data['password_new1']))
        user_to_edit.first_name = form.cleaned_data['first_name']
        user_to_edit.last_name_name = form.cleaned_data['last_name']
        user_to_edit.email = form.cleaned_data['email']
        if form.cleaned_data['password_new1']:
            user_to_edit.set_password(form.cleaned_data['password_new1'])
        user_to_edit.save()
        user_profile.country = form.cleaned_data['country']
        user_profile.city = form.cleaned_data['city']
        user_profile.age = form.cleaned_data['age']
        user_profile.bio = form.cleaned_data['bio']
        if 'image' in request.FILES:
            user_profile.image = request.FILES['image']
        user_profile.save()
        return redirect(reverse('user_home', args={user_to_edit.username}))
    except ObjectDoesNotExist as e:
        print("iihinkb ocmle comes here")
        # if the user doesn't exist in the database, it redirects to the global stream page
        return redirect(reverse('user_home', args={user_to_edit.username}))


#################################################################################################
@login_required
def profile(request, username):
    context = {}
    login_user = request.user
    try:
        userobj = User.objects.get(username=username)
        user_profile = userobj.profile
        # get the list of all followers for users
        follower_list = login_user.profile.follow.all()
        only_id_list = []
        for z in follower_list:
            only_id_list.append(z.user.id)
        id = userobj.id
        ##########################################################
        form = CommentForm(request.POST or None)
        if 'post' in request.POST and request.method != 'GET':
            context = add_posts(request, userobj, username)
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
                # here part cut
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
                # here part 2 cut
            context = {'post_comm': post_comm, 'user_posts': all_posts, 'details': username, 'id': id,
                       'profile': user_profile, 'follow_list': only_id_list, 'log_user_page': userobj, 'form': form}
            ###############################################################################

            return render(request, 'Profile.html', context)
    except ObjectDoesNotExist as e:
        # if the user doesn't exist in the database, it redirects to the global stream page
        return redirect(reverse('global'))


#######################################################################################################
@login_required
def user_home(request, username):
    context = {}
    try:
        artist_info = User.objects.get(username=username)
        current_artist = Artist.objects.get(artist=artist_info)
        # get list of bands he belongs to
        bands = Band.objects.filter(creator=current_artist.id)

        login_user = request.user
        # artistobj = User.objects.get(username=username)
        profile = artist_info.artist
        context['details'] = username
        context['profile'] = profile
        context['user'] = artist_info
        context['bands'] = bands
        return render(request, 'user_home.html', context)
    except ObjectDoesNotExist as e:
        return render(request, 'welcome.html', {})


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


######################################################################################################
@login_required()
def band_page(request):
    context = {}
    context['user'] = request.user.username
    return render(request, 'bandpage.html', context)


##########################################fuctions to join and create#############################################
@login_required()
def join(request):
    context = {}
    errors = []

    form = BandForm(request.POST or None)

    context['errors'] = errors
    context['form'] = form
    return render(request, 'band_join.html', context)

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
    # new_band = Band(band_name = band_name)
    # new_band.save()

    band_info = form.cleaned_data['band_info']
    city = form.cleaned_data['city']
    creator = request.user

    new_band = Band(band_name=band_name, band_info=band_info, city=city, creator=creator)
    if 'image' in request.FILES:
        new_band.image = request.FILES['image']

    new_band.save()

    creator.artist.member.add(new_band)
    print("successfully joined band")

    context['current_artist'] = creator
    context['band'] = new_band
    context['message'] = 'created'

    return redirect(reverse('user_band_list'))


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
    context['bands'] = bands
    return render(request, 'user_home.html', context)


# fundtion to get list of available bands
@login_required()
def band_list(request):
    context = {}
    errors = []
    context['errors'] = errors

    # get list of bands he belongs to
    bands = Band.objects.all()
    print("successfully " + str(bands))
    context['bands'] = bands
    context['errors'] = errors
    return render(request, 'band_list.html', context)


##################################################################################################
@login_required()
def calendar(request):
    return render(request, 'user_calendar.html', {})

@login_required()
def band_calendar(request,band_id):
    context = {}
    print("band_calendar : " + band_id)
    band = Band.objects.get(id=band_id)
    context['bandid'] = band_id
    context['band'] = band
    return render(request, 'user_calendar.html', context)


#################################################################################################
@login_required()
def event(request):
    all_events = Event.objects.all()
    get_event_types = Event.objects.only('event_type')

    # if filters applied then get parameter and filter based on condition else return object
    if request.GET:
        event_arr = []
        if request.GET.get('event_type') == "all":
            all_events = Event.objects.all()
        else:
            all_events = Event.objects.filter(event_type__icontains=request.GET.get('event_type'))

        for i in all_events:
            event_sub_arr = {}
            event_sub_arr['title'] = i.event_name
            start_date = datetime.datetime.strptime(str(i.start_date.date()), "%Y-%m-%d").strftime("%Y-%m-%d")
            end_date = datetime.datetime.strptime(str(i.end_date.date()), "%Y-%m-%d").strftime("%Y-%m-%d")
            event_sub_arr['start'] = start_date
            event_sub_arr['end'] = end_date
            event_arr.append(event_sub_arr)
        return HttpResponse(json.dumps(event_arr))

    context = {
        "events": all_events,
        "get_event_types": get_event_types,

    }
    return render(request, 'user_calendar.html', context)


###################################################################################################
#band page with it events associated with band
@login_required()
def band_events(request, band_id):
    if not band_id:
        redirect(reverse('user_home', args=request.user.username))
    try:
        band = Band.objects.get(id = band_id)
        events = Event.objects.filter(band_name = band.id)
        context = {}
        context['events'] = events
        context['band_id'] = band_id
        print("the size of event list is ", len(events))
        return render(request, 'bandpage.html', context)
    except ObjectDoesNotExist:
        return redirect(reverse('band_list'))


@login_required()
def create_event(request):
    print("successfully received get")

    if request.method == 'GET':
        print("event if")
        context = {'form': EventForm()}
        return render(request, 'event_create.html', context)

    form = EventForm(request.POST)

    context = {}
    errors = []
    context['errors'] = errors
    context['form'] = form
    current_artist = Artist.objects.get(artist=request.user.id)
    user_bands = Band.objects.filter(creator = current_artist.id)
    print('the size of list is ', len(user_bands))
    if not form.is_valid():
        print("form not valid")
        errors = 'Something went wrong, try again.'
        context['errors'] = errors
        return render(request, 'event_create.html', context)

    band_name = form.cleaned_data['band_name']
    band_name_instance = Band.objects.get(band_name = band_name)
    # new_band.save()
    print('type is ', type(band_name))
    event_name = form.cleaned_data['event_name']
    start_date = form.cleaned_data['start_date']
    end_date = form.cleaned_data['end_date']
    event_type = form.cleaned_data['event_type']
    creator = request.user

    new_event = Event(band_name= band_name_instance, event_name=event_name, start_date=start_date,
                      end_date=end_date, event_type=event_type, creator=creator)

    new_event.save()
    print("successfully created event")

    context['current_artist'] = creator
    context['new_event'] = new_event
    context['message'] = 'created'

    return redirect(reverse('event_lists'))


# fundtion to get list of available bands
@login_required()
def event_lists(request):
    print("successfully entered event_list")

    events = []
    context = {}
    errors = []
    context['errors'] = errors

    current_artist = Artist.objects.get(artist=request.user.id)
    # get list of bands he belongs to
    bands = Band.objects.filter(creator=current_artist.id)
    print("Current Artist" + str(current_artist.artist.username), len(bands))

    for band in bands:
        event_band = Event.objects.filter(band_name = band.id)
        print("Current Artist" ,len(event_band))

        event_band_list = []
        for each in event_band:
            event_band_list.append(each)
        print("length ", len(event_band_list))
        events.append(event_band_list)
        # events[band.id] = event_band_list

    context['events'] = events
    #a = json.dumps(events)
    print("the the the ", type(events))
    context['bands'] = bands
    return render(request, 'events_home.html', context)

@login_required()
def event_lists1(request):
    #print("successfully entered event_list")

    events = []
    context = {}
    errors = []
    context['errors'] = errors
    current_artist = Artist.objects.get(artist=request.user.id)
    #print("Current Artist" + str(current_artist.artist.username))
    # get list of bands he belongs to
    bands = Band.objects.filter(creator=current_artist.id)
    for band in bands:
        event_band = Event.objects.filter(band_name=band)
        event_band_list = []
        for each in event_band:
            event_band_list.append(each)
        print("length ", len(event_band_list))
        events.append(event_band_list)
        # events[band.id] = event_band_list

    context['events'] = events
    # a = json.dumps(events)
    print("the the the ", type(events))
    context['bands'] = bands
    j = render_to_string('events.json', context)
    json.dumps(j)
    return HttpResponse(j, content_type="application/json")


        # # fundtion to get list of available bands
    # def band_list(request):
    #     context = {}
    #     errors = []
    #     context['errors'] = errors
    #
    #     # get list of bands he belongs to
    #     bands = Band.objects.all()
    #     print("successfully " + str(bands))
    #     context['bands'] = bands
    #     context['errors'] = errors
    #     return render(request, 'band_list.html', context)
