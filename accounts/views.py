# accounts/views.py
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth import authenticate, get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
import json
import jwt
import random
import string
from django.views.decorators.http import require_http_methods

# Use Django's default User model
User = get_user_model()

@csrf_exempt
@require_http_methods(["POST"])
def register(request):
    try:
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')
        first_name = data.get('first_name', '')
        last_name = data.get('last_name', '')
        
        if not email or not password:
            return JsonResponse({'error': 'Email and password are required'}, status=400)
        
        if User.objects.filter(email=email).exists():
            return JsonResponse({'error': 'User with this email already exists'}, status=400)
        
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        
        return JsonResponse({
            'status': 'success',
            'access': access_token,
            'refresh': str(refresh),
            'user': {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name
            }
        }, status=201)
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def login(request):
    try:
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return JsonResponse({'error': 'Email and password are required'}, status=400)
        
        user = authenticate(username=email, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            
            return JsonResponse({
                'status': 'success',
                'access': access_token,
                'refresh': str(refresh),
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name
                }
            }, status=200)
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)
            
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def google_login(request):
    try:
        data = json.loads(request.body)
        token = data.get('token')
        email = data.get('email')
        first_name = data.get('first_name', '')
        last_name = data.get('last_name', '')
        
        if not token or not email:
            return JsonResponse({'error': 'Token and email are required'}, status=400)
        
        try:
            decoded = jwt.decode(token, options={"verify_signature": False})
            token_email = decoded.get('email')
            if token_email != email:
                return JsonResponse({'error': 'Email mismatch'}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'Invalid token: {str(e)}'}, status=400)
        
        user = User.objects.filter(email=email).first()
        if user:
            if first_name:
                user.first_name = first_name
            if last_name:
                user.last_name = last_name
            user.save()
        else:
            password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
        
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        
        return JsonResponse({
            'access': access_token,
            'refresh': str(refresh),
            'user': {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'username': user.username
            }
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def profile(request):
    return JsonResponse({'message': 'Profile endpoint'}, status=200)

@csrf_exempt
def forgot_password(request):
    try:
        data = json.loads(request.body)
        email = data.get('email')
        
        if not email:
            return JsonResponse({'error': 'Email is required'}, status=400)
        
        user = User.objects.filter(email=email).first()
        if user:
            # In a real application, you would send a password reset email
            return JsonResponse({
                'status': 'success',
                'message': 'Password reset link sent to your email'
            }, status=200)
        else:
            return JsonResponse({
                'status': 'success',
                'message': 'Password reset link sent to your email'
            }, status=200)
            
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)