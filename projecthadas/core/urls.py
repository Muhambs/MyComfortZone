from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('registerpatient/', views.registerpatient.as_view(), name='register_patient'),
    path('registerdoctor/', views.registerdoctor.as_view(), name='register_doctor'),
    path('loginpatient/', views.patientlogin, name='patient_login'),
    path('logindoctor/', views.doctorlogin, name='doctor_login'),
    path('logout/', views.logout_user, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profilealternate/', views.another_profile, name='another_profile'),
    path('contact/', views.contact, name='contact'),
    path('chat/', views.chat, name='chat'),
    path('<str:room>/', views.room, name='room'),
    path('chat/checkview', views.checkview, name='checkview'),
    path('send', views.send, name='send'),
    path('getMessages/<str:room>/', views.getMessages, name='getMessages'),

]
