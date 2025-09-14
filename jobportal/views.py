from django.http import JsonResponse
# jobportal/views.py

def health_check(request):
    return JsonResponse({"status": "ok"}, status=200)

def api_info(request):
    return JsonResponse({
        "message": "Job Portal API is running",
        "version": "1.0",
        "endpoints": {
            "auth": "/auth/",
            "register": "/auth/register/",
            "login": "/auth/login/",
            "google-login": "/auth/google-login/",
            "profile": "/auth/profile/",
            "forgot-password": "/auth/forgot-password/"
        }
    })