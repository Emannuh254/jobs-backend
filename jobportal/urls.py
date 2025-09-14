# jobportal/urls.py
from django.contrib import admin
from django.urls import path, include
from django.views.decorators.http import require_GET
from django.http import HttpResponse
from .views import health_check, api_info

@require_GET
def favicon(request):
    """Handle favicon requests"""
    return HttpResponse(status=204)

urlpatterns = [
    # Health check and API info
    path('', health_check, name='health_check'),
    path('api-info/', api_info, name='api_info'),
    
    # Django admin
    path('admin/', admin.site.urls),
    
    # Authentication endpoints
    path('auth/', include('accounts.urls')),
    
    # Static files
    path('favicon.ico', favicon),
]