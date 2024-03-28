from django.urls import path
from django.contrib.auth import views as auth_view
from .views import home, profile, logout_user
from . import views
from .views import RegisterView

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', RegisterView.as_view(template_name='users/register.html'), name='register'),
    path('profile/', views.profile, name='profile'),
    path('login/', auth_view.LoginView.as_view(template_name='users/login.html'), name="login"),
    path('logout/', logout_user, name="logout"),
    path('contact/', views.contact, name='contact'),  # Assuming you have a view named `contact`

]
