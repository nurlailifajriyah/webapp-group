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

# Create your models here.

# this class contains information about individual artists
# this class is a profile which extends User model
class Artist(models.Model):
    artist_id = models.OneToOneField(User, on_delete=models.CASCADE, related_name='artist')
    bio = models.TextField(max_length=140, blank=True)
    address1 = models.CharField(max_length=30, blank=True)
    address2 = models.CharField(max_length=30, blank=True)
    zipcode = models.IntegerField(blank=True, null=True, validators=[MaxValueValidator(99999)])
    birth_date = models.DateField(null=True, blank=True)
    image = models.ImageField(upload_to='tempo/media', blank=True)


    def __unicode__(self):
        return self.text

    # creates an artist profile after registration
    @receiver(post_save, sender=User)
    def create_artist_profile(sender, instance, created, **kwargs):
        if created:
            Artist.objects.create(artist_id=instance)

    # saves the profile of the artist
    @receiver(post_save, sender=User)
    def save_artist_profile(sender, instance, **kwargs):
        instance.artist.save()


# this class contains information about the bands
# it has a many2many fiels for Artist (members)
class Band(models.Model):
    band_name = models.OneToOneField(User, on_delete=models.CASCADE, related_name='band')
    band_info = models.TextField(max_length=140, blank=True) #like a bio
    city = models.CharField(max_length=30, blank=True)
    zipcode = models.IntegerField(blank=True, null=True, validators=[MaxValueValidator(99999)])
    created_date = models.DateField(null=True, blank=True)
    image = models.ImageField(upload_to='tempo/media', blank=True)
    # this field allows this artist to be a member of certain groups
    artist = models.ManyToManyField(Artist, related_name='member', symmetrical=False)

    def __unicode__(self):
        return self.text

