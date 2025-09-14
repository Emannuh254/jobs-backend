from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('google-login/', views.GoogleLoginView.as_view(), name='google-login'),
    path('forgot-password/', views.ForgotPasswordView.as_view(), name='forgot-password'),
]