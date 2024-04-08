from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail
from django.db import transaction
from django.http import JsonResponse, Http404, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, DetailView
from django.urls import reverse_lazy
from .decorates import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import *
from .models import *
from django.db.models import Avg, Count
import logging
logger = logging.getLogger(__name__)

def home(request):
    return render(request, 'home.html')

class registerpatient(CreateView):
    template_name = 'registerpatient.html'
    form_class = registerpatient
    success_url = reverse_lazy('patientlogin')

    def get_success_url(self):
        messages.success(self.request, "User has been created, please login with your username and password")
        return super().get_success_url()
    def form_valid(self, form):
        with transaction.atomic():
            user = form.save()
            Profile.objects.create(user=user, is_patient=True)
            group, _ = Group.objects.get_or_create(name='patient')
            user.groups.add(group)
            messages.success(self.request, "User has been created, please login with your username and password")
        return super().form_valid(form) and redirect('home')

class registerdoctor(CreateView):
    template_name = 'registerdoctor.html'
    form_class = registerdoctor
    success_url = reverse_lazy('doctorlogin')

    def form_valid(self, form):
        with transaction.atomic():
            user = form.save()
            Profile.objects.create(user=user, is_doctor=True)
            group, _ = Group.objects.get_or_create(name='doctor')
            user.groups.add(group)
            messages.success(self.request, 'Doctor account has been created successfully')
        return super().form_valid(form) and redirect('home')


def logoutview(request):
    logout(request)
    return redirect('home')
@csrf_exempt
@login_required
def profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'profile.html', {'form': form, 'profile': profile})
@login_required
def editprofile(request):
    profile = request.user.userprofile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'editprofile.html', {'form': form})

def patientlogin(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                try:
                    profile = Profile.objects.get(user=user)
                except Profile.DoesNotExist:
                    messages.error(request, "This account does not have a profile.")
                    return render(request, 'patientlogin.html', {'form': form})
                if profile.is_patient:
                    login(request, user)
                    return redirect('profile')
                else:
                    messages.error(request, "Access denied: User is not a patient.")
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'patientlogin.html', {'form': form})

def doctorlogin(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                try:
                    profile = Profile.objects.get(user=user)
                except Profile.DoesNotExist:
                    messages.error(request, "This account does not have a profile.")
                    return render(request, 'doctorlogin.html', {'form': form})

                if profile.is_doctor:
                    login(request, user)
                    return redirect('profile')
                else:
                    messages.error(request, "Access denied: User is not a doctor.")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Error validating the form")
    else:
        form = AuthenticationForm()
    return render(request, 'doctorlogin.html', {'form': form})


def contact(request):
    return render(request,'home.html')

@login_required
def chat(request):
    return render(request,'homechat.html')

def room(request, room):
    room_details = get_object_or_404(Room, name=room)
    username = request.GET.get('username')
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

import logging
logger = logging.getLogger(__name__)


@login_required
def book_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user
            appointment.save()
            messages.success(request, 'Appointment booked successfully!')
            return redirect('book_appointment')
    else:
        form = AppointmentForm()
    return render(request, 'book_appointment.html', {'form': form})

@login_required
def view_appointments(request):
    appointments = Appointment.objects.filter(doctor=request.user).order_by('appointment_time')
    accepted_appointments_ids = appointments.filter(status='accepted').values_list('id', flat=True)
    return render(request, 'view_appointments.html', {
        'appointments': appointments,
        'accepted_appointments_ids': accepted_appointments_ids,
    })


@login_required
def update_appointment_status(request, appointment_id, status):
    appointment = get_object_or_404(Appointment, id=appointment_id, doctor=request.user)

    if status == 'rejected':
        appointment.delete()
    elif status == 'accepted':
        appointment.status = 'accepted'
        appointment.save()

    return redirect('view_appointments')

@require_POST
def delete_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, doctor=request.user)  # Check ownership
    appointment.delete()
    return redirect('view_appointments')

@login_required
def media(request):
    if request.method == 'POST':
        form = MediaForm(request.POST, request.FILES)
        if form.is_valid():
            media_item = form.save(commit=False)
            media_item.doctor = request.user
            media_item.save()
            messages.success(request, 'Media uploaded successfully!')
            return redirect('media')
        else:
            messages.error(request, 'Error uploading file. Please check the form.')
    else:
        form = MediaForm()
    media_list = Media.objects.all()
    return render(request, 'media.html', {'form': form, 'media_list': media_list})
@login_required
def upload_media(request):
    if request.method == 'POST':
        form = MediaForm(request.POST, request.FILES)
        if form.is_valid():
            media = form.save(commit=False)
            media.doctor = request.user
            media.save()
            messages.success(request, 'Media uploaded successfully!')
            return redirect('media')
        else:
            messages.error(request, 'Error uploading file. Please check the form.')
            return render(request, 'media.html', {'form': form})
    else:
        form = MediaForm()
    return render(request, 'media.html', {'form': form})

@login_required
@require_POST
def delete_media(request, media_id):
    media = get_object_or_404(Media, id=media_id)
    if request.user.profile.is_doctor:
        media.delete()
        return redirect('media')
    else:
        return redirect('media')

class UserDetailView(DetailView):
    model = User
    template_name = 'user_detail.html'
    context_object_name = 'profile_user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.get_object().profile
        return context

class UserDetailView(DetailView):
    model = User
    template_name = 'user_detail.html'
    context_object_name = 'profile_user'

    def dispatch(self, request, *args, **kwargs):
        profile_user = self.get_object()
        if profile_user.profile.is_patient and request.user.is_authenticated and not request.user.profile.is_doctor:
            return HttpResponseForbidden("You are not allowed to view other patients' profiles.")
        return super().dispatch(request, *args, **kwargs)

def update_appointment_status(request, appointment_id, status):
    appointment = get_object_or_404(Appointment, id=appointment_id, doctor=request.user)
    patient_email = appointment.patient.email

    if status == 'rejected' or status == 'accepted':
        message = f"Your appointment has been {status}."
        Notification.objects.create(receiver=appointment.patient, message=message)

    if status == 'rejected':
        appointment.delete()
        send_mail(
            'Appointment Update',
            'Your appointment has been rejected.',
            settings.EMAIL_HOST_USER,
            [patient_email],
            fail_silently=False,
        )
    elif status == 'accepted':
        appointment.status = 'accepted'
        appointment.save()
        send_mail(
            'Appointment Update',
            'Your appointment has been accepted.',
            settings.EMAIL_HOST_USER,
            [patient_email],
            fail_silently=False,
        )

    return redirect('view_appointments')


class Notification(models.Model):
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Notification for {self.receiver.username}"

def about(request):
    return render(request, 'about.html')


def submit_rating(request):

    if request.method == 'POST':

        form= WebsiteRatingForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for your feedback!')
            return redirect('home')  # Redirect to a confirmation page or back to home
    else:
        form = WebsiteRatingForm()
    return render(request, 'submit_rating.html', {'form': form})

def ratings_summary (request):

    avg_rating = WebsiteRating.objects.aggregate(Avg('rating'))['rating__avg']
    total_ratings = WebsiteRating.objects.aggregate(Count('id'))['id__count']
    rating_summaries = WebsiteRating.objects.all().order_by('-id')  # Assuming recent first
    return render(request, 'ratings_summary.html', {
        'avg_rating': avg_rating,
        'total_ratings': total_ratings,
        'rating_summaries': rating_summaries
    })

@login_required
def view_doctors(request):
    if not request.user.profile.is_doctor:

        doctors = Profile.objects.filter(is_doctor=True)
        for doctor in doctors:  # Debugging: Print out the values to inspect them
            print(f"Doctor: {doctor.user.username}, Education: {doctor.education}, Room chat: {doctor.roomchat}")
        return render(request, 'view_doctors.html', {'doctors': doctors})
    else:
        return render(request, 'error.html', {'message': 'Only patients can view doctors profiles.'})



@login_required
def report_bug(request):
    if request.method == 'POST':
        form = BugReportForm(request.POST)

        if form.is_valid():
            bug_report = form.save(commit=False)
            bug_report.user = request.user
            bug_report.save()
            return redirect('home')

    else:
        form = BugReportForm()
    return render(request, 'report_bug.html', {'form': form})

def view_bug_reports(request):

    bug_reports = BugReport.objects.all().order_by('-created_at')
    return render(request, 'view_bug_reports.html', {'bug_reports': bug_reports})


def delete_bug_report(request, bug_id):

    bug_report = get_object_or_404(BugReport, id=bug_id)

    bug_report.delete()

    messages.success(request, "Bug report successfully deleted.")
    return redirect('view_bug_reports')



