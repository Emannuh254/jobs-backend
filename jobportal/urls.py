# jobportal/urls.py
from django.contrib import admin
from django.urls import path, include
from .views import api_info

urlpatterns = [
    path('', api_info, name='api-info'),
    path('admin/', admin.site.urls),
    path('auth/', include('accounts.urls')),
    # Add other app URLs here
]