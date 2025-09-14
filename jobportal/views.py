from django.http import JsonResponse

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