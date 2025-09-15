from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin panel
    path('admin/', admin.site.urls),
    
    # Include allauth URLs for authentication
    path('auth/', include('allauth.urls')),
    
    # Include accounts app URLs
    path('api/accounts/', include('accounts.urls')),
    
    # Include other app URLs
    path('api/jobs/', include('jobs.urls')),
    path('api/referrals/', include('referrals.urls')),
    path('api/applications/', include('applications.urls')),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)