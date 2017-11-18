from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import *
from .forms import *
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

