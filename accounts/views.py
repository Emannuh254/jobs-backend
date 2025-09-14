# accounts/views.py
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views import View
import json

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
            from django.contrib.auth.models import User
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
            
            # Return success response
            return JsonResponse({
                'status': 'success',
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