from multiprocessing.reduction import register

from django.urls import path
from . import views
from django.contrib.auth import views as auth_view

from .views import RegisterView, home, logout_user

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', RegisterView.as_view(template_name='users/register.html'), name='register'),
    path('profile/', views.profile, name='profile'),
    path('login/', auth_view.LoginView.as_view(template_name='users/login.html'), name="login"),
    path('logout/', logout_user, name="logout"),
    path('home/', home, name="home"),

]
