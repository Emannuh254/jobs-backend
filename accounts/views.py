from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate, login, logout
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from .models import User
from .serializers import UserSerializer, RegisterSerializer
import jwt
from rest_framework_simplejwt.tokens import RefreshToken
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

# ==============================
# Register with email verification
# ==============================
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save(is_active=False)  # Require email verification
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        activation_link = f"{settings.FRONTEND_URL}/verify.html?uid={uid}&token={token}"

        send_mail(
            "Verify your account",
            f"Click to verify your account: {activation_link}",
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
        )


# ==============================
# Email verification endpoint
# ==============================
class VerifyEmailView(APIView):
    permission_classes = [AllowAny]

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


# ==============================
# Login with JWT
# ==============================
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(request, email=email, password=password)

        if user and user.is_active:
            login(request, user)
            refresh = RefreshToken.for_user(user)
            return Response({
                "user": UserSerializer(user).data,
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            }, status=200)
        return Response({"error": "Invalid credentials or email not verified"}, status=400)


# ==============================
# Logout
# ==============================
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"success": "Logged out"}, status=200)


# ==============================
# Google Login
# ==============================
class GoogleLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        token = request.data.get("token")
        try:
            # Verify Google ID token
            idinfo = id_token.verify_oauth2_token(
                token, google_requests.Request(),
                settings.GOOGLE_OAUTH2_CLIENT_ID
            )

            email = idinfo["email"]
            first_name = idinfo.get("given_name", "")
            last_name = idinfo.get("family_name", "")
            picture = idinfo.get("picture", "")

            # Get or create user
            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    "username": email,
                    "first_name": first_name,
                    "last_name": last_name,
                    "google_id": idinfo["sub"],
                    "google_name": f"{first_name} {last_name}",
                    "google_picture": picture,
                    "is_active": True,
                }
            )

            # Generate JWT
            refresh = RefreshToken.for_user(user)
            return Response({
                "user": UserSerializer(user).data,
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            }, status=200)

        except Exception as e:
            return Response({"error": str(e)}, status=400)
