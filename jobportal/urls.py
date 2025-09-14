# jobportal/urls.py
from django.contrib import admin
from django.urls import path, include
from .views import api_info, health_check
from django.views.decorators.http import require_GET
from django.http import HttpResponse

@require_GET
def favicon(request):
    return HttpResponse(status=204)

urlpatterns = [
    path('', health_check, name='health_check'),  # Root URL handled by health_check
    path('api-info/', api_info, name='api-info'),  # Moved api_info to a different path
    path('admin/', admin.site.urls),  # Admin URLs (only once)
    path('auth/', include('accounts.urls')),  # Authentication URLs
    path('favicon.ico', favicon),  # Favicon handler
    # Add other app URLs here
]