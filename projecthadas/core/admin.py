from django.contrib import admin
from .models import *
from .models import Appointment

admin.site.register(Room)
admin.site.register(Message)
admin.site.register(doctor)
admin.site.register(patient)
admin.site.register(UserProfuile)
admin.site.register(Appointment)