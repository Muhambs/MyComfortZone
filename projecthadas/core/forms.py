from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import UserProfuile

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