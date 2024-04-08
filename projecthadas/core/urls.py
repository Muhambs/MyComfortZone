from django.conf.urls.static import static
from django.urls import path, include
from . import views
from .views import *

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('registerpatient/', views.registerpatient.as_view(), name='registerpatient'),
    path('registerdoctor/', views.registerdoctor.as_view(), name='registerdoctor'),
    path('patientlogin/', views.patientlogin, name='patientlogin'),
    path('doctorlogin/', views.doctorlogin, name='doctorlogin'),
    path('logout/', views.logoutview, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('editprofile/', views.editprofile, name='editprofile'),
    path('contact/', views.contact, name='contact'),
    path('chat/', views.chat, name='chat'),
    path('media/', views.media, name='media'),
    path('chat/checkview', views.checkview, name='checkview'),
    path('send', views.send, name='send'),
    path('media/upload/', views.upload_media, name='upload_media'),
    path('media/delete/<int:media_id>/', delete_media, name='delete_media'),
    path('getMessages/<str:room>/', views.getMessages, name='getMessages'),
    path('book_appointment/', views.book_appointment, name='book_appointment'),
    path('view_appointments/', views.view_appointments, name='view_appointments'),
    path('delete_appointment/<int:appointment_id>/', views.delete_appointment, name='delete_appointment'),
    path('update_appointment_status/<int:appointment_id>/<str:status>/', views.update_appointment_status, name='update_appointment_status'),
    path('view_appointments/', view_appointments, name='view_appointment'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('doctors/', view_doctors, name='view_doctors'),
    path('report-bug/', report_bug, name='report_bug'),
    path('view_bug_reports/', view_bug_reports, name='view_bug_reports'),
    path('delete_bug_report/<int:bug_id>/', delete_bug_report, name='delete_bug_report'),
    path('ratings-summary/', ratings_summary, name='ratings_summary'),
    path('submit-rating/', submit_rating, name='submit_rating'),
    path('<str:room>/', views.room, name='room'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)