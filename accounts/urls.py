from django.urls import path
from accounts.views import (
    RegisterView, 
    LoginView, 
    ProfileView, 
    GoogleLoginView, 
    ForgotPasswordView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('google-login/', GoogleLoginView.as_view(), name='google-login'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
]