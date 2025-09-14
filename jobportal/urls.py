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
    # ... existing URLs
    path('favicon.ico', favicon),
]

urlpatterns = [
    path('', api_info, name='api-info'),
    path('admin/', admin.site.urls),
    path('admin/', admin.site.urls),
    path('', health_check, name='health_check'),
    path('auth/', include('accounts.urls')),
    # Add other app URLs here
]