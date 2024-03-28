from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

#Dania Ighbaria
def home(request):
    return render(request, 'users/home.html')

def contact(request):
    return render(request, 'users/contact.html')
#Rana Younis
class RegisterView(CreateView):
    mode = User
    form_class = UserRegisterForm
    template_name = 'register.html'
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('profile')

def logout_user(request):
    logout(request)
    return redirect('login')


@login_required()
def profile(request):
    return render(request, 'users/profile.html')

#Shhd Jbareen
def login_user(request):
    if request.method == "GET":
        return render(request, 'contact.html')
    elif request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile')
        else:
            print("wrong username or password")
            return redirect('contact')
