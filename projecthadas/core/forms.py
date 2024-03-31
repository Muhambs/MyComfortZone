from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

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

