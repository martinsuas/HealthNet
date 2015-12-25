__author__ = 'Zach'
from django import forms
from django.contrib.auth.models import User
from Users.models import Profile, PatientProfile

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password')


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = (
            'first_name',
            'middle_name',
            'last_name',
            'email',
            'home_phone_number',
            'work_phone_number',
            'cell_phone_number',
        )


class PatientProfileForm(forms.ModelForm):
    class Meta:
        model = PatientProfile
        fields = (
            'date_of_birth',
            'home_address',
        )


class EditProfile(forms.Form):
    first_name = forms.CharField(label='First Name:', widget=forms.TextInput(attrs={'class': 'form-control'}))
    middle_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    home_phone_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    work_phone_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    cell_phone_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))


class EditPatient(forms.Form):
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control'}))
    home_address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))


