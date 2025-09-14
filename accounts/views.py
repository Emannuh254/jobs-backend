from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views import View
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
import json
import random
import string

# Try to import Google auth libraries with error handling
try:
    from google.oauth2 import id_token
    from google.auth.transport import requests
    GOOGLE_AUTH_AVAILABLE = True
except ImportError:
    GOOGLE_AUTH_AVAILABLE = False

User = get_user_model()

def get_json_data(request):
    """Safely parse JSON from request body"""
    try:
        return json.loads(request.body)
    except json.JSONDecodeError:
        return None

def generate_unique_username(email):
    """Generate a unique username from email"""
    base_username = email.split('@')[0]
    username = base_username
    counter = 1
    while User.objects.filter(username=username).exists():
        username = f"{base_username}{counter}"
        counter += 1
    return username

class RegisterView(View):
    @csrf_exempt
    def post(self, request):
        data = get_json_data(request)
        if data is None:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
            
        email = data.get('email')
        password = data.get('password')
        first_name = data.get('first_name', '')
        last_name = data.get('last_name', '')
        
        if not email or not password:
            return JsonResponse({'error': 'Email and password are required'}, status=400)
        
        if User.objects.filter(email=email).exists():
            return JsonResponse({'error': 'User with this email already exists'}, status=400)
        
        # Generate a unique username
        username = generate_unique_username(email)
        
        user = User.objects.create_user(
            username=username,
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
                'last_name': user.last_name,
                'username': user.username
            }
        }, status=201)

class LoginView(View):
    @csrf_exempt
    def post(self, request):
        data = get_json_data(request)
        if data is None:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
            
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return JsonResponse({'error': 'Email and password are required'}, status=400)
        
        # Use the custom backend to authenticate by email
        user = authenticate(request, email=email, password=password)
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
                    'last_name': user.last_name,
                    'username': user.username
                }
            }, status=200)
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)

class GoogleLoginView(View):
    @csrf_exempt
    def post(self, request):
        if not GOOGLE_AUTH_AVAILABLE:
            return JsonResponse({'error': 'Google authentication libraries not available'}, status=500)
            
        data = get_json_data(request)
        if data is None:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
            
        token = data.get('token')
        
        if not token:
            return JsonResponse({'error': 'Token is required'}, status=400)
        
        try:
            # Verify Google token with proper signature validation
            idinfo = id_token.verify_oauth2_token(
                token, 
                requests.Request(), 
                settings.GOOGLE_OAUTH2_CLIENT_ID
            )
            
            # Validate issuer
            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                return JsonResponse({'error': 'Invalid token issuer'}, status=400)
                
            email = idinfo['email']
            first_name = idinfo.get('given_name', '')
            last_name = idinfo.get('family_name', '')
            
        except Exception as e:
            return JsonResponse({'error': f'Invalid token: {str(e)}'}, status=400)
        
        user = User.objects.filter(email=email).first()
        if user:
            # Update existing user info
            user.first_name = first_name
            user.last_name = last_name
            user.save()
        else:
            # Generate a unique username
            username = generate_unique_username(email)
            # Create new user with random password
            password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
            user = User.objects.create_user(
                username=username,
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
                'last_name': user.last_name,
                'username': user.username
            }
        })

class ProfileView(View):
    @csrf_exempt
    def get(self, request):
        try:
            # Authenticate user using JWT
            authenticator = JWTAuthentication()
            auth_result = authenticator.authenticate(request)
            
            if auth_result is None:
                # Try to get the token from the Authorization header manually
                auth_header = request.META.get('HTTP_AUTHORIZATION')
                if auth_header and auth_header.startswith('Bearer '):
                    token = auth_header.split(' ')[1]
                    try:
                        # Validate the token
                        validated_token = authenticator.get_validated_token(token)
                        user = authenticator.get_user(validated_token)
                        if user.is_active:
                            return JsonResponse({
                                'status': 'success',
                                'user': {
                                    'id': user.id,
                                    'email': user.email,
                                    'first_name': user.first_name,
                                    'last_name': user.last_name,
                                    'username': user.username,
                                }
                            }, status=200)
                    except Exception as e:
                        raise AuthenticationFailed("Invalid token")
                raise AuthenticationFailed("Authentication credentials were not provided")
            
            user, _ = auth_result  # user object and token
            return JsonResponse({
                'status': 'success',
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'username': user.username,
                }
            }, status=200)
        except AuthenticationFailed as e:
            return JsonResponse({'error': str(e)}, status=401)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

class ForgotPasswordView(View):
    @csrf_exempt
    def post(self, request):
        data = get_json_data(request)
        if data is None:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
            
        email = data.get('email')
        
        if not email:
            return JsonResponse({'error': 'Email is required'}, status=400)
        
        user = User.objects.filter(email=email).first()
        if user:
            # Generate password reset token
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            # Create reset link (in production, use your domain)
            reset_link = f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}/"
            
            # Send email
            send_mail(
                'Password Reset Request',
                f'Click the link to reset your password: {reset_link}',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            
            return JsonResponse({
                'status': 'success',
                'message': 'Password reset link sent to your email'
            }, status=200)
        else:
            # Don't reveal if email exists or not
            return JsonResponse({
                'status': 'success',
                'message': 'Password reset link sent to your email'
            }, status=200)