from django import forms
from .models import *

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
        if User.objects.filter(username__exact = username):
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
