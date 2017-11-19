from django import forms
from .models import *
import datetime
from django.forms import ModelChoiceField
from datetimewidget.widgets import DateTimeWidget, DateWidget, TimeWidget

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

class UserModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
         return obj.name


class SongForm(forms.Form):
    name = forms.CharField(max_length=140)
    image = forms.ImageField(required=False, widget=forms.FileInput())


class BandForm(forms.Form):
    bandname = forms.CharField(max_length=20)
    band_info = forms.CharField(max_length=20, label='Band Info')
    city = forms.CharField(max_length=20, label='City')
    image = forms.ImageField(required=False, widget=forms.FileInput())

    # valdiation for username
    def clean_username(self):
        band_name = self.cleaned_data.get('bandname')
        if len(Band.objects.filter(username__exact=band_name)) >= 1:
            raise forms.ValidationError("Band name already taken")
        return band_name


class ProfileEditForm(forms.Form):
    first_name = forms.CharField(max_length=20, label='First Name')
    last_name = forms.CharField(max_length=20, label='Last Name')
    email = forms.EmailField(max_length=200, label='Email')
    password_new1 = forms.CharField(max_length=200, label='Password', widget=forms.PasswordInput(), required=False)
    password_new2 = forms.CharField(max_length=200, label='Confirm Password', widget=forms.PasswordInput(),
                                    required=False)
    city = forms.CharField(max_length=100, required=False)
    country = forms.CharField(max_length=100, required=False)
    age = forms.IntegerField(required=False)
    bio = forms.CharField(max_length=200, required=False)
    image = forms.ImageField(required=False, widget=forms.FileInput())

    def clean(self):
        cleaned_data = super(ProfileEditForm, self).clean()
        password1 = cleaned_data.get('password_new1')
        password2 = cleaned_data.get('password_new22')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return cleaned_data


class EventForm(forms.Form):
    event_name = forms.CharField(max_length=20, label='Event_name')
    start_date = forms.DateField(widget=DateWidget(usel10n=True, bootstrap_version=3))
    end_date = forms.DateField(widget=DateWidget(usel10n=True, bootstrap_version=3))
    event_type = forms.CharField(max_length=10)


    def clean(self):
        cleaned_data = super(EventForm, self).clean()
        start_date = self.cleaned_data.get('start_date')
        end_date = self.cleaned_data.get('end_date')
        if start_date != None and end_date != None:
            if end_date < start_date:
                raise forms.ValidationError("Invalid date entered")
        return cleaned_data

    def clean_event_name(self):
        event_name = self.cleaned_data.get('event_name')
        return event_name

    def clean_event_type(self):
        event_name = self.cleaned_data.get('event_type')
        return event_name

    def clean_start_date(self):
        start_date = self.cleaned_data.get('start_date')
        if start_date < datetime.date.today():
            raise forms.ValidationError("Enter a date in future")
        return start_date

    def clean_end_date(self):
        start_date = self.cleaned_data.get('start_date')
        end_date = self.cleaned_data.get('end_date')
        if end_date < datetime.date.today():
            raise forms.ValidationError("enter date in future please")
        # if end_date < start_date:
        #     raise forms.ValidationError("Invalid date entered")
        return end_date

