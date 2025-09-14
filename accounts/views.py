# accounts/views.py
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views import View
import json
import jwt  # You need to install PyJWT: pip install PyJWT
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

@csrf_exempt
class GoogleLoginView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            token = data.get('token')
            email = data.get('email')
            first_name = data.get('first_name', '')
            last_name = data.get('last_name', '')
            
            if not token or not email:
                return JsonResponse({'error': 'Token and email are required'}, status=400)
            
            # Decode the token without verification (not secure for production)
            try:
                # The token is a JWT, we decode it without verification
                decoded = jwt.decode(token, options={"verify_signature": False})
                # Extract the email from the token and compare with the one sent
                token_email = decoded.get('email')
                if token_email != email:
                    return JsonResponse({'error': 'Email mismatch'}, status=400)
            except Exception as e:
                return JsonResponse({'error': f'Invalid token: {str(e)}'}, status=400)
            
            # Check if user exists
            user = User.objects.filter(email=email).first()
            if user:
                # Update user's name if provided
                if first_name:
                    user.first_name = first_name
                if last_name:
                    user.last_name = last_name
                user.save()
            else:
                # Create a new user
                # Generate a random password since the user is signing in with Google
                import random
                import string
                password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
                user = User.objects.create_user(
                    username=email,
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name
                )
            
            # Generate a JWT token for our app
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

# Keep your existing RegisterView
@csrf_exempt
class RegisterView(View):
    def post(self, request):
        try:
            # Parse JSON data from request body
            data = json.loads(request.body)
            
            # Extract required fields
            email = data.get('email')
            password = data.get('password')
            first_name = data.get('first_name', '')
            last_name = data.get('last_name', '')
            
            # Validate required fields
            if not email or not password:
                return JsonResponse({
                    'error': 'Email and password are required'
                }, status=400)
            
            # Check if user already exists
            if User.objects.filter(email=email).exists():
                return JsonResponse({
                    'error': 'User with this email already exists'
                }, status=400)
            
            # Create new user
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            
            # Return success response
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
            return JsonResponse({
                'error': 'Invalid JSON data'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'error': str(e)
            }, status=500)