from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('registerpatient/', views.registerpatient.as_view(), name='register_patient'),
    path('registerdoctor/', views.registerdoctor.as_view(), name='register_doctor'),
    path('loginpatient/', views.patientlogin, name='patient_login'),
    path('logindoctor/', views.doctorlogin, name='doctor_login'),
    path('logout/', views.logoutview, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('editprofile/', views.editprofile, name='editprofile'),
    path('contact/', views.contact, name='contact'),
    path('chat/', views.chat, name='chat'),
    path('chat/checkview', views.checkview, name='checkview'),
    path('send', views.send, name='send'),
    path('getMessages/<str:room>/', views.getMessages, name='getMessages'),
    path('book_appointment/', views.book_appointment, name='book_appointment'),
    path('view_appointments/', views.view_appointments, name='view_appointments'),
    path('delete_appointment/<int:appointment_id>/', views.delete_appointment, name='delete_appointment'),
    path('update_appointment_status/<int:appointment_id>/<str:status>/', views.update_appointment_status, name='update_appointment_status'),
    path('<str:room>/', views.room, name='room'),

]
