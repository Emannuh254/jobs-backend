import requests
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .serializers import UserSerializer

class GoogleLoginView(APIView):
    def post(self, request):
        token = request.data.get("token")

        # Verify Google token
        google_url = "https://oauth2.googleapis.com/tokeninfo"
        resp = requests.get(google_url, params={"id_token": token})

        if resp.status_code != 200:
            return Response({"error": "Invalid Google token"}, status=400)

        data = resp.json()
        email = data.get("email")
        first_name = data.get("given_name", "")
        last_name = data.get("family_name", "")
        google_id = data.get("sub")
        google_name = f"{first_name} {last_name}"
        google_picture = data.get("picture", "")

        if not email:
            return Response({"error": "Google account has no email"}, status=400)

        # Get or create user
        user, created = User.objects.get_or_create(email=email, defaults={
            "username": email,
            "first_name": first_name,
            "last_name": last_name,
            "google_id": google_id,
            "google_name": google_name,
            "google_picture": google_picture,
        })

        if not created:
            user.google_id = google_id
            user.google_name = google_name
            user.google_picture = google_picture
            user.save()

        # Issue JWT tokens
        refresh = RefreshToken.for_user(user)

        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": UserSerializer(user).data
        })
