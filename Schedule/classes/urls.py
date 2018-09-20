from django.urls import path, include

from . import views
from classes.views import HomeView, LogoutView
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LogoutView, LoginView

urlpatterns = [
    path('', HomeView.as_view(), name='homepage'),
    path('register', views.signup, name='signup'),
    path('login', views.LoginView.as_view(template_name='classes/login.html'), name='login'),
    path('logout', views.LogoutView.as_view(), name='logout'),
    path('delete', views.delete, name='delete'),
    path('ajax/validate_course/', views.validate_course, name='validate_course'),
    
]