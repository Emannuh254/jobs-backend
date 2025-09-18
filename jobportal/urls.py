from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse


def home(request):
    return JsonResponse({"message": "Job Portal API is running 🚀"})

urlpatterns = [
    path("admin/", admin.site.urls),
    
    # Your custom accounts app (API endpoints for JWT, registration, etc.)
    path("auth/", include("accounts.urls")),
    
    # Django-allauth routes (Google OAuth2 etc.)
    path("accounts/", include("allauth.urls")),
    

    path('panel/', include('panel.urls')),
    path("", home),
    
    
    # Jobs and other apps
]
