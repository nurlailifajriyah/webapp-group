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
    image = models.ImageField(upload_to='tempo/images/band', blank=True)
    members = models.ManyToManyField(
        User,
        through='ArtistInBand',
        through_fields=('band', 'member'),
    )

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
    image = models.ImageField(upload_to='tempo/images/artist', blank=True)

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


class ArtistInBand(models.Model):
    band = models.ForeignKey(Band, verbose_name='band', related_name='band')
    member = models.ForeignKey(User, verbose_name='band_member', default="", related_name='band_member')
    class Meta:
        unique_together = ('band', 'member',)

class SongList(models.Model):
    name = models.CharField(max_length=140, blank=True)
    creation_time = models.DateTimeField(auto_now=True)
    band = models.ForeignKey(Band, related_name='band_song_list', default ='')
    image = models.ImageField(upload_to='tempo/images/song_list', blank=True)
    def __unicode__(self):
        return u'{0}'.format(self.name)
    def __str__(self):
        return u'{0}'.format(self.name)

class Song(models.Model):
    name = models.CharField(max_length=140, blank=True)
    creation_time = models.DateTimeField(auto_now=True)
    band = models.ForeignKey(Band, related_name='band_song', default='')
    image = models.ImageField(upload_to='tempo/images/song', blank=True)

class SongInList(models.Model):
    list = models.ForeignKey(SongList, related_name='list')
    song = models.ForeignKey(Song, related_name='song_in_list')

class Track(models.Model):
    name = models.TextField(max_length=140, blank=True)
    type = models.TextField(max_length=140, blank=True)
    audio_file = models.FileField(upload_to='tempo/audio/track', blank=True)
    version_number = models.IntegerField(default=1, blank=True, null=True)
    creation_time = models.DateTimeField(auto_now=True)
    song = models.ForeignKey(Song, related_name='song',  default ='')

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.__unicode__()

    # Returns all recent additions
    @staticmethod
    def get_tracks(song_id,time="1970-01-01T00:00+00:00"):
        try:
            song = Song.objects.get(id=song_id)
        except:
            return Track()
        return Track.objects.order_by('-creation_time').filter(creation_time__gt=time, song=song).distinct()
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
    event_name = models.CharField(max_length=255,null=False,blank=False)
    start_date = models.DateTimeField(null=False,blank=False)
    end_date = models.DateTimeField(null=False,blank=False)
    event_type = models.CharField(max_length=10,null=True,blank=True)
    list = models.ForeignKey(SongList, related_name='songlist_event', null=True, blank=True)

    def __str__(self):
        return self.event_name