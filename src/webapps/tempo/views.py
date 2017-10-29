# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import login
from django.contrib.auth.decorators import login_required


# Create your views here.
def home(request):
    return render(request, 'welcome.html')

####################################LOGIN######################################################
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
            #post_comm = {}
            post_comm = []
            for k in all_posts:
                comm = Comment.objects.filter(post=k).order_by('-ctime')
                post_comm.append(comm)
                #here part cut
            context['post_comm'] = post_comm
            #######################################################
            # return render(request, 'post_comm.json',context, content_type='application/json')
            # return render(request, 'user_posts.json', context, content_type='application/json')
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

