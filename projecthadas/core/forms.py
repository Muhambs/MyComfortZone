from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django import forms
from django.core.exceptions import ValidationError
from django.forms import DateTimeInput
from django.utils import timezone

from .models import *


class registerpatient(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']

class registerdoctor(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']


class logindoctor(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','password1']
class loginpatient(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','password1']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'location', 'dob', 'profile_image', 'education','roomchat']
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ProfileForm, self).__init__(*args, **kwargs)
        if user and not user.profile.is_doctor:
            self.fields.pop('roomchat', None)
        else:
            pass

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor', 'appointment_time', 'note']
        widgets = {
            'appointment_time': DateTimeInput(attrs={'type': 'text', 'class': 'datetimepicker'}),
        }
    def clean_appointment_time(self):
        appointment_time = self.cleaned_data.get('appointment_time')
        if appointment_time and appointment_time < timezone.now():
            raise ValidationError("The appointment time cannot be in the past. Please choose a future date and time.")
        return appointment_time

    def __init__(self, *args, **kwargs):
        super(AppointmentForm, self).__init__(*args, **kwargs)
        self.fields['doctor'].queryset = User.objects.filter(profile__is_doctor=True)
        self.fields['appointment_time'].input_formats = ['%Y-%m-%d %H:%M:%S']


class MediaForm(forms.ModelForm):
    class Meta:
        model = Media
        fields = ['title', 'file', 'link']

class WebsiteRatingForm(forms.ModelForm):
    class Meta:
        model = WebsiteRating
        fields = ['rating', 'comment']


class BugReportForm(forms.ModelForm):
    class Meta:
        model = BugReport
        fields = ['title', 'description']