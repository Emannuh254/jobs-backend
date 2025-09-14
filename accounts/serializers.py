from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)
    referral_code = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2', 'referral_code', 'first_name', 'last_name')
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords don't match."})
        return attrs
    
    def create(self, validated_data):
        referral_code = validated_data.pop('referral_code', None)
        password = validated_data.pop('password')
        
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=password,
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        
        # Process referral if code provided
        if referral_code:
            try:
                referrer = User.objects.get(referral_code=referral_code)
                # Create referral record
                from referrals.models import Referral
                Referral.objects.create(
                    referrer=referrer,
                    referred=user,
                    points_earned=10
                )
                # Award points to referrer
                referrer.points += 10
                referrer.save()
            except User.DoesNotExist:
                pass  # Invalid referral code
        
        return user

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 
                 'referral_code', 'points', 'google_id', 'google_name', 'google_picture')

class GoogleLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, validators=[validate_password])
    google_token = serializers.CharField(write_only=True)
    
    def validate_google_token(self, token):
        try:
            from google.oauth2 import id_token
            from google.auth.transport import requests
            from django.conf import settings
            
            idinfo = id_token.verify_oauth2_token(
                token, 
                requests.Request(), 
                settings.GOOGLE_OAUTH2_CLIENT_ID
            )
            
            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise serializers.ValidationError("Invalid issuer")
                
            return idinfo
            
        except Exception as e:
            raise serializers.ValidationError(f"Google token verification failed: {str(e)}")
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        google_token = attrs.get('google_token')
        
        token_data = self.validate_google_token(google_token)
        
        if token_data['email'] != email:
            raise serializers.ValidationError("Email does not match Google token")
        
        try:
            user = User.objects.get(email=email)
            
            if not user.google_id:
                user.google_id = token_data['sub']
                user.google_name = token_data.get('name', '')
                user.google_picture = token_data.get('picture', '')
                user.save()
            
            if user.has_usable_password() and not user.check_password(password):
                raise serializers.ValidationError({
                    "email": "Account already exists. Please sign in with your password."
                })
                
            if not user.has_usable_password():
                user.set_password(password)
                user.save()
                
        except User.DoesNotExist:
            base_username = email.split('@')[0]
            username = base_username
            counter = 1
            while User.objects.filter(username=username).exists():
                username = f"{base_username}{counter}"
                counter += 1
                
            name = token_data.get('name', '')
            first_name, last_name = '', ''
            if name:
                name_parts = name.split()
                first_name = name_parts[0] if name_parts else ''
                last_name = ' '.join(name_parts[1:]) if len(name_parts) > 1 else ''
                
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                google_id=token_data['sub'],
                google_name=name,
                google_picture=token_data.get('picture', '')
            )
        
        from rest_framework_simplejwt.tokens import RefreshToken
        refresh = RefreshToken.for_user(user)
        
        return {
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'referral_code': user.referral_code,
                'points': user.points,
                'google_id': user.google_id,
                'google_name': user.google_name,
                'google_picture': user.google_picture
            }
        }