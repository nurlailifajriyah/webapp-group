from django import forms
from .models import *
from django.forms import ModelChoiceField
from datetimewidget.widgets import DateTimeWidget, DateWidget, TimeWidget
from PIL import Image
from django.utils.translation import ugettext as _
import datetime
import pytz

class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=20)
    first_name = forms.CharField(max_length=20, label='First Name')
    last_name = forms.CharField(max_length=20, label='Last Name')
    email = forms.EmailField(max_length=200, label='Email')
    password1 = forms.CharField(max_length=200, label='Password', widget=forms.PasswordInput())
    password2 = forms.CharField(max_length=200, label='Confirm Password', widget=forms.PasswordInput())
    city = forms.CharField(max_length=100, required=False)
    country = forms.CharField(max_length=100, required=False)
    zipcode = forms.IntegerField(required=False)
    bio = forms.CharField(max_length=200, required=False)
    age = forms.IntegerField(required=False)

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return cleaned_data

    # valdiation for username
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is already taken")
        return username

    # validation for email
    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).count():
            raise forms.ValidationError("Email is already registered")
        return email


class SongListForm(forms.Form):
    name = forms.CharField(max_length=140)

class SongForm(forms.Form):
    name = forms.CharField(max_length=140,widget=forms.TextInput(attrs={'class': 'form-control'}))
    image = forms.ImageField(required=False, widget=forms.FileInput(), label='Song\'s Chord')

    def clean_image(self):
        image = self.cleaned_data.get('image', False)

        if image:
            img = Image.open(image)
            w, h = img.size

            # validate dimensions
            max_width = max_height = 1024
            if w > max_width or h > max_height:
                raise forms.ValidationError(
                    _('Please use an image that is smaller or equal to '
                      '%s x %s pixels.' % (max_width, max_height)))

            # validate content type
            main, sub = image.content_type.split('/')
            if not (main == 'image' and sub.lower() in ['jpeg', 'pjpeg', 'png', 'jpg']):
                raise forms.ValidationError(_('Please use a JPEG or PNG image.'))

            # validate file size
            if len(image) > (1 * 1024 * 1024):
                raise forms.ValidationError(_('Image file too large ( maximum 1mb )'))
            return image


class BandForm(forms.Form):
    bandname = forms.CharField(max_length=20)
    band_info = forms.CharField(max_length=20, label='Band Info')
    city = forms.CharField(max_length=20, label='City')
    image = forms.ImageField(required=False, widget=forms.FileInput())

    # valdiation
    def clean_bandname(self):
        band_name = self.cleaned_data.get('bandname')
        if len(Band.objects.filter(band_name__exact=band_name)) >= 1:
            raise forms.ValidationError("Band name already taken")
        return band_name

    def clean_image(self):
        image = self.cleaned_data.get('image', False)

        if image:
            img = Image.open(image)
            w, h = img.size

            # validate dimensions
            max_width = max_height = 1024
            if w > max_width or h > max_height:
                raise forms.ValidationError(
                    _('Please use an image that is smaller or equal to '
                      '%s x %s pixels.' % (max_width, max_height)))

            # validate content type
            main, sub = image.content_type.split('/')
            if not (main == 'image' and sub.lower() in ['jpeg', 'pjpeg', 'png', 'jpg']):
                raise forms.ValidationError(_('Please use a JPEG or PNG image.'))

            # validate file size
            if len(image) > (1 * 1024 * 1024):
                raise forms.ValidationError(_('Image file too large ( maximum 1mb )'))
            return image


class ProfileEditForm(forms.Form):
    first_name = forms.CharField(max_length=20, label='First Name',widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=20, label='Last Name',widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(max_length=200, label='Email',widget=forms.TextInput(attrs={'class': 'form-control'}))
    password_new1 = forms.CharField(max_length=200, label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=False)
    password_new2 = forms.CharField(max_length=200, label='Confirm Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                    required=False)
    city = forms.CharField(max_length=100, required=False,widget=forms.TextInput(attrs={'class': 'form-control'}))
    country = forms.CharField(max_length=100, required=False,widget=forms.TextInput(attrs={'class': 'form-control'}))
    age = forms.IntegerField(required=False,widget=forms.TextInput(attrs={'class': 'form-control'}))
    bio = forms.CharField(max_length=200, required=False,widget=forms.TextInput(attrs={'class': 'form-control'}))
    image = forms.ImageField(required=False, widget=forms.FileInput())

    def clean(self):
        cleaned_data = super(ProfileEditForm, self).clean()
        password1 = cleaned_data.get('password_new1')
        password2 = cleaned_data.get('password_new22')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return cleaned_data

    def clean_image(self):
        image = self.cleaned_data.get('image', False)

        if image:
            img = Image.open(image)
            w, h = img.size

            # validate dimensions
            max_width = max_height = 1024
            if w > max_width or h > max_height:
                raise forms.ValidationError(
                    _('Please use an image that is smaller or equal to '
                      '%s x %s pixels.' % (max_width, max_height)))

            # validate content type
            main, sub = image.content_type.split('/')
            if not (main == 'image' and sub.lower() in ['jpeg', 'pjpeg', 'png', 'jpg']):
                raise forms.ValidationError(_('Please use a JPEG or PNG image.'))

            # validate file size
            if len(image) > (1 * 1024 * 1024):
                raise forms.ValidationError(_('Image file too large ( maximum 1mb )'))
            return image


class EventForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.band_id = kwargs.pop('band_id')
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields['song_list'] = ModelChoiceField(queryset=SongList.objects.filter(band_id=self.band_id),
                                                    required=False)

    event_name = forms.CharField(max_length=20, label='Event_name',
                                 widget=forms.TextInput(attrs={'class': 'form-control'}))
    start_date = forms.DateTimeField(
        widget=DateTimeWidget(usel10n=True, bootstrap_version=3, attrs={'class': 'form-control'}), required=True)
    end_date = forms.DateTimeField(
        widget=DateTimeWidget(usel10n=True, bootstrap_version=3, attrs={'class': 'form-control'}), required=True)
    event_type = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'class': 'form-control'}))

    def clean(self):
        cleaned_data = super(EventForm, self).clean()
        start_date = self.cleaned_data.get('start_date')
        end_date = self.cleaned_data.get('end_date')

        if start_date != None and end_date != None:
            if end_date < start_date:
                raise forms.ValidationError("Invalid date entered: End date must be after start date")
        return cleaned_data

    def clean_event_name(self):
        event_name = self.cleaned_data.get('event_name')
        return event_name

    def clean_event_type(self):
        event_name = self.cleaned_data.get('event_type')
        return event_name

    def clean_start_date(self):
        utc = pytz.UTC
        start_date = self.cleaned_data.get('start_date')
        # start_time_utc = start_date.replace(tzinfo=utc)
        if start_date < datetime.datetime.now().replace(tzinfo=utc):
            raise forms.ValidationError("Please enter a date in future")
        return start_date

    def clean_end_date(self):
        utc = pytz.UTC
        end_date = self.cleaned_data.get('end_date')
        # end_time_utc = end_date.replace(tzinfo=utc)
        if end_date < datetime.datetime.now().replace(tzinfo=utc):
            raise forms.ValidationError("Please enter date in future")
        return end_date

