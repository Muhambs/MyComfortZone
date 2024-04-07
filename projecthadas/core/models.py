from django.contrib.auth.models import User
from django.db import models
from datetime import datetime
from django.utils.timezone import now


class Room(models.Model):
    name = models.CharField(max_length=1000)
class Message(models.Model):
    value = models.CharField(max_length=1000000)
    date = models.DateTimeField(default=datetime.now, blank=True)
    user = models.CharField(max_length=1000000)
    room = models.CharField(max_length=1000000)

class patient(models.Model):
    user=models.OneToOneField(User,null=True,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    marks = models.CharField(max_length=100)

class doctor(models.Model):
    user=models.OneToOneField(User,null=True,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    file = models.FileField(max_length=100)



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_patient = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)
    bio = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    dob = models.DateField(null=True, blank=True, default=now)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    education = models.TextField(blank=True, null=True)
    roomchat = models.CharField(max_length=255, blank=True, null=True)
    def __str__(self):
        return f"{self.user.username}'s profile"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_patient = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)
    bio = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    dob = models.DateField(null=True, blank=True, default=now)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    education = models.TextField(blank=True, null=True)
    roomchat = models.CharField(max_length=255, blank=True, null=True)
    def __str__(self):
        return f"{self.user.username}'s profile"


class Appointment(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    )

    patient = models.ForeignKey(User, related_name='appointments_as_patient', on_delete=models.CASCADE)
    doctor = models.ForeignKey(User, related_name='appointments_as_doctor', on_delete=models.CASCADE)
    appointment_time = models.DateTimeField(default=now)
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default='pending')
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.patient.username} appointment with {self.doctor.username} on {self.appointment_time}"

class Media(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='media/', blank=True, null=True)  # For uploading files
    link = models.URLField(max_length=500, blank=True, null=True)  # For storing external links
    doctor = models.ForeignKey(User, related_name='uploaded_media', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
class MyModel(models.Model):
    image = models.ImageField(upload_to='images/')


class WebsiteRating(models.Model):
    RATING_CHOICES = [
        (1, 'Very Poor'),
        (2, 'Poor'),
        (3, 'Average'),
        (4, 'Good'),
        (5, 'Excellent'),
    ]
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username if self.user else 'Anonymous'} - {self.get_rating_display()}"

class BugReport(models.Model):
        user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bug_reports")
        title = models.CharField(max_length=255)
        description = models.TextField()
        created_at = models.DateTimeField(auto_now_add=True)

        def __str__(self):
            return self.title

