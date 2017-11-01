# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.validators import MaxValueValidator
from django.db.models import Max
from django.db import models
from django.contrib.auth.models import User

# signals allow the Artist automatically create
# and update user instances
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.db import models


class Artist(models.Model):
    artist = models.OneToOneField(User, on_delete=models.CASCADE, related_name='artist')
    bio = models.TextField(max_length=140, blank=True)
    city = models.CharField(max_length=30, blank=True)
    country = models.CharField(max_length=30, blank=True)
    zipcode = models.IntegerField(blank=True, null=True, validators=[MaxValueValidator(99999)])
    age = models.IntegerField(default=1, blank=True, null=True)
    # birth_date = models.DateField(null=True, blank=True)
    image = models.ImageField(upload_to='tempo/media', blank=True)


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


class Band(models.Model):
    band_name = models.OneToOneField(User, on_delete=models.CASCADE, related_name='band')
    band_info = models.TextField(max_length=140, blank=True) #like a bio
    city = models.CharField(max_length=30, blank=True)
    zipcode = models.IntegerField(blank=True, null=True, validators=[MaxValueValidator(99999)])
    created_date = models.DateField(null=True, blank=True)
    image = models.ImageField(upload_to='tempo/media', blank=True)
    # this field allows this artist to be a member of certain groups
    artist = models.ManyToManyField(Artist, related_name='member', symmetrical=False)

    #TODO Songlist and Song


class Track(models.Model):
    name = models.TextField(max_length=140, blank=True)
    type = models.TextField(max_length=140, blank=True)
    audio_file = models.FileField(upload_to='tempo/audio', blank=True) #TODO audiofield
    version_number = models.IntegerField(default=1, blank=True, null=True)



