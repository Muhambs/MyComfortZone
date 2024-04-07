from django.contrib import admin
from .models import *
from .models import Appointment

admin.site.register(Room)
admin.site.register(Message)
admin.site.register(doctor)
admin.site.register(patient)
admin.site.register(UserProfile)
admin.site.register(Appointment)

class WebsiteRatingAdmin(admin.ModelAdmin):
    list_display = ['user', 'rating', 'comment']
    list_filter = ['rating']
    search_fields = ['comment', 'user__username']