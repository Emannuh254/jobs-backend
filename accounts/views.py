from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from .models import User
from .serializers import UserSerializer, RegisterSerializer
from rest_framework.views import APIView
import jwt

# Register with email verification
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        activation_link = f"{settings.FRONTEND_URL}/verify.html?uid={uid}&token={token}"

        send_mail(
            "Verify your account",
            f"Click to verify your account: {activation_link}",
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
        )


# Email verification endpoint
class VerifyEmailView(APIView):
    def get(self, request):
        uid = request.GET.get("uid")
        token = request.GET.get("token")

        try:
            user = User.objects.get(pk=force_str(urlsafe_base64_decode(uid)))
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({"error": "Invalid link"}, status=400)

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({"success": "Account verified"})
        return Response({"error": "Invalid or expired token"}, status=400)


# Login
class LoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(request, email=email, password=password)

        if user and user.is_active:
            login(request, user)
            return Response({"user": UserSerializer(user).data}, status=200)
        return Response({"error": "Invalid credentials or email not verified"}, status=400)


# Logout
class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({"success": "Logged out"}, status=200)
