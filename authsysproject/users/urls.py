from multiprocessing.reduction import register

from django.urls import path
from . import views
from django.contrib.auth import views as auth_view

from .views import RegisterView, home, logout_user

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('logout/', logout_user, name="logout"),

]