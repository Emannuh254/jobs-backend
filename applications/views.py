# accounts/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.views import View
import json
import jwt
from django.conf import settings
from datetime import datetime, timedelta
import random
import string

# Helper function to generate JWT token
def generate_jwt_token(user):
    payload = {
        'user_id': user.id,
        'username': user.username,
        'exp': datetime.utcnow() + timedelta(days=1),
        'iat': datetime.utcnow()
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token

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
        
        # Generate JWT token
        token = generate_jwt_token(user)
        
        return JsonResponse({
            'status': 'success',
            'message': 'User created successfully',
            'token': token,
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
        
        user = authenticate(request, username=email, password=password)
        if user is not None:
            # Generate JWT token
            token = generate_jwt_token(user)
            
            return JsonResponse({
                'status': 'success',
                'message': 'Login successful',
                'token': token,
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
@require_http_methods(["GET", "POST"])
def profile(request):
    # This would typically require authentication
    # For now, just return a placeholder
    return JsonResponse({'message': 'Profile endpoint'}, status=200)

@csrf_exempt
@require_http_methods(["POST"])
def google_login(request):
    try:
        data = json.loads(request.body)
        token = data.get('token')
        
        if not token:
            return JsonResponse({'error': 'Token is required'}, status=400)
        
        # In a real implementation, you would verify the token with Google
        # For now, we'll just extract the email from the token
        try:
            # This is a simplified version - in production, use Google's auth libraries
            decoded = jwt.decode(token, options={"verify_signature": False})
            email = decoded.get('email')
            
            if not email:
                return JsonResponse({'error': 'Invalid token'}, status=400)
            
            # Check if user exists
            user = User.objects.filter(email=email).first()
            if not user:
                # Create a new user with a random password
                random_password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
                user = User.objects.create_user(
                    username=email,
                    email=email,
                    password=random_password,
                    first_name=decoded.get('given_name', ''),
                    last_name=decoded.get('family_name', '')
                )
            
            # Generate JWT token
            jwt_token = generate_jwt_token(user)
            
            return JsonResponse({
                'status': 'success',
                'message': 'Google login successful',
                'token': jwt_token,
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name
                }
            }, status=200)
            
        except Exception as e:
            return JsonResponse({'error': f'Token verification failed: {str(e)}'}, status=400)
            
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def forgot_password(request):
    try:
        data = json.loads(request.body)
        email = data.get('email')
        
        if not email:
            return JsonResponse({'error': 'Email is required'}, status=400)
        
        # Check if user exists
        user = User.objects.filter(email=email).first()
        if user:
            # In a real application, you would send a password reset email
            # For now, we'll just return a success message
            return JsonResponse({
                'status': 'success',
                'message': 'Password reset link sent to your email'
            }, status=200)
        else:
            # Don't reveal that the user doesn't exist
            return JsonResponse({
                'status': 'success',
                'message': 'Password reset link sent to your email'
            }, status=200)
            
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)