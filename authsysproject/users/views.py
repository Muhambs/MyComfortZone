from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout




def logout_user(request):
    logout(request)
    return redirect('login')


@login_required()
def profile(request):
    return render(request, 'users/profile.html')

