from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from django.contrib import messages
from django.template.context_processors import request
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .decorates import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import *
from .models import Room,Message
def home(request):
    return render(request, 'home.html')

class registerpatient(CreateView):
    template_name = 'PatientRegisterView.html'  # Assuming the same template is used for both patient and doctor registration
    form_class = RegisterViewpatient  # Assuming you have defined a PatientRegisterForm
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        # Save the user
        user = form.save()

        # Assign the user to the 'Patient' group
        group = Group.objects.get(name='Patient')  # Assuming you have a group named 'Patient'
        user.groups.add(group)

        messages.success(self.request, 'Patient account has been created successfully')
        return super().form_valid(form)

class registerdoctor(CreateView):
    template_name = 'DoctorRegisterView.html'  # Assuming the same template is used for both patient and doctor registration
    form_class = RegisterViewdoctor  # Assuming you have defined a DoctorRegisterForm
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        # Save the user
        user = form.save()

        # Assign the user to the 'Doctor' group
        group = Group.objects.get(name='Doctor')  # Assuming you have a group named 'Doctor'
        user.groups.add(group)

        messages.success(self.request, 'Doctor account has been created successfully')
        return super().form_valid(form)


def logout_user(request):
    logout(request)
    return redirect('home.html')


@login_required
@doctor_required
def profile(request):
    return render(request, 'profile.html')
@login_required
@patient_required
def another_profile(request):
    return render(request, 'another_profile.html')

def patientlogin(request):
    if request.method == "POST":
        form = loginpatient(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('profile')  # Redirect to patient profile upon successful login
            else:
                print("Wrong username or password")  # Log the error (or handle it in a better way)
    else:
        form = loginpatient()
    return render(request, 'patientlogin.html', {'form': form})

def doctorlogin(request):
    if request.method == "POST":
        form = logindoctor(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('profile')  # Redirect to doctor profile upon successful login
            else:
                print("Wrong username or password")  # Log the error (or handle it in a better way)
    else:
        form = logindoctor()
    return render(request, 'doctorlogin.html', {'form': form})


def contact(request):
    return render(request,'home.html')

@login_required
def chat(request):
    return render(request,'homechat.html')

def room(request, room):
    username = request.GET.get('username')
    room_details = Room.objects.get(name=room)
    return render(request, 'room.html', {
        'username': username,
        'room': room,
        'room_details': room_details
    })

def checkview(request):
    room = request.POST['room_name']
    username = request.POST['username']

    if Room.objects.filter(name=room).exists():
        return redirect('/'+room+'/?username='+username)
    else:
        new_room = Room.objects.create(name=room)
        new_room.save()
        return redirect('/'+room+'/?username='+username)


def send(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']

    new_message = Message.objects.create(value=message, user=username, room=room_id)
    new_message.save()
    return HttpResponse('Message sent successfully')

def getMessages(request, room):
    room_details = Room.objects.get(name=room)

    messages = Message.objects.filter(room=room_details.id)
    return JsonResponse({"messages":list(messages.values())})