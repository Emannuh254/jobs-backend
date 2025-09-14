# jobportal/views.py
from django.http import JsonResponse
from django.views.decorators.http import require_GET

@require_GET
def health_check(request):
    """Health check endpoint for monitoring"""
    return JsonResponse({
        "status": "ok",
        "message": "Service is running",
        "version": "1.0.0"
    })

@require_GET
def api_info(request):
    """API information endpoint"""
    return JsonResponse({
        "name": "Job Portal API",
        "version": "1.0.0",
        "endpoints": {
            "auth": {
                "register": "/auth/register/",
                "login": "/auth/login/",
                "google-login": "/auth/google-login/",
                "forgot-password": "/auth/forgot-password/"
            }
        }
    })