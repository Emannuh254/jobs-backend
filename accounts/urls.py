from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('profile/', views.profile, name='profile'),
    path('google-login/', views.google_login, name='google-login'),
    path('forgot-password/', views.forgot_password, name='forgot-password'),
]