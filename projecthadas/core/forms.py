from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import UserProfuile, Appointment, doctor, Media


class RegisterViewpatient(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']

class RegisterViewdoctor(UserCreationForm):
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
        model = UserProfuile
        fields = ['bio', 'location', 'dob', 'profile_image', 'education']
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
        }


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor', 'appointment_time', 'note']
        # Assuming 'appointment_time' is the field for the datetime of the appointment

    def clean_appointment_time(self):
        appointment_time = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'class': 'datetimepicker'}))
        if appointment_time and appointment_time < timezone.now():
            # Raises a validation error if the appointment_time is in the past
            raise ValidationError("The appointment time cannot be in the past. Please choose a future date and time.")
        return appointment_time

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['appointment_time'].widget.attrs.update({'class': 'datetimepicker'})


class MediaForm(forms.ModelForm):
    class Meta:
        model = Media
        fields = ['title', 'file', 'link']