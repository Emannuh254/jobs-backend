from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    
    # Your custom accounts app (API endpoints for JWT, registration, etc.)
    path("auth/", include("accounts.urls")),
    
    # Django-allauth routes (Google OAuth2 etc.)
    path("accounts/", include("allauth.urls")),
    
    # Jobs and other apps
    path("jobs/", include("jobs.urls")),
]
