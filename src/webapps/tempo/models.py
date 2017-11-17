# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.validators import MaxValueValidator
from django.db.models import Max
from django.db import models
from django.contrib.auth.models import User
from django.template.loader import get_template


# signals allow the Artist automatically create
# and update user instances
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.db import models


class Band(models.Model):
    band_name = models.CharField(max_length=30, blank=True)
    creator = models.ForeignKey(User, default='', blank=False, related_name='artist_creator')
    band_info = models.TextField(max_length=140, blank=True) #like a bio
    city = models.CharField(max_length=30, blank=True)
    zipcode = models.IntegerField(blank=True, null=True, validators=[MaxValueValidator(99999)])
    created_date = models.DateField(null=True, blank=True)
    image = models.ImageField(upload_to='tempo/image', blank=True)
    # this field allows this artist to be a member of certain groups

    def __str__(self):
        return self.band_name


class Artist(models.Model):
    artist = models.OneToOneField(User, on_delete=models.CASCADE, related_name='artist')
    bio = models.TextField(max_length=140, blank=True)
    city = models.CharField(max_length=30, blank=True)
    country = models.CharField(max_length=30, blank=True)
    zipcode = models.IntegerField(blank=True, null=True, validators=[MaxValueValidator(99999)])
    age = models.IntegerField(default=1, blank=True, null=True)
    # birth_date = models.DateField(null=True, blank=True)
    image = models.ImageField(upload_to='tempo/images', blank=True)
    member = models.ManyToManyField(Band, related_name='member_of', symmetrical=False)

    # # creates an artist profile after registration
    # @receiver(post_save, sender=User)
    # def create_artist_profile(sender, instance, created, **kwargs):
    #     if created:
    #         Artist.objects.create(artist_id=instance)
    #
    # # saves the profile of the artist
    # @receiver(post_save, sender=User)
    # def save_artist_profile(sender, instance, **kwargs):
    #     instance.artist.save()



class SongList(models.Model):
    name = models.TextField(max_length=140, blank=True)
    creation_time = models.DateTimeField(auto_now=True)


class Song(models.Model):
    name = models.TextField(max_length=140, blank=True)
    songlist = models.ManyToManyField(SongList)
    creation_time = models.DateTimeField(auto_now=True)


class Track(models.Model):
    name = models.TextField(max_length=140, blank=True)
    type = models.TextField(max_length=140, blank=True)
    audio_file = models.FileField(upload_to='tempo/audio', blank=True)
    version_number = models.IntegerField(default=1, blank=True, null=True)
    creation_time = models.DateTimeField(auto_now=True)

    #TODO foreignkey to song

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.__unicode__()

    # Returns all recent additions
    @staticmethod
    def get_tracks(time="1970-01-01T00:00+00:00"):
        return Track.objects.order_by('-creation_time').filter(creation_time__gt=time).distinct()
        # Returns all recent additions

    @property
    def html(self):
        template = get_template('tracks/tracklist.html')
        context = {}
        context['trackid'] = self.id
        context['trackname'] = self.name
        context['audiofile'] = self.audio_file
        context['track'] = self
        # https://djangobook.com/templates-in-views/
        return template.render(context)

    @staticmethod
    def get_max_time():
        return Track.objects.all().aggregate(Max('creation_time'))[
                   'creation_time__max'] or "1970-01-01T00:00+00:00"



class Event(models.Model):
    band_name = models.ForeignKey(Band, default='', blank=False, related_name='band_event')
    creator = models.ForeignKey(User, default='', blank=False, related_name='event_creator')
    event_id = models.AutoField(primary_key=True)
    event_name = models.CharField(max_length=255,null=True,blank=True)
    start_date = models.DateTimeField(null=True,blank=True)
    end_date = models.DateTimeField(null=True,blank=True)
    event_type = models.CharField(max_length=10,null=True,blank=True)

    def __str__(self):
        return self.event_name