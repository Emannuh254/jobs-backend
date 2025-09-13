from rest_framework import serializers
from .models import Referral

class ReferralSerializer(serializers.ModelSerializer):
    referrer = serializers.StringRelatedField(read_only=True)
    referred = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Referral
        fields = '__all__'
        read_only_fields = ('referrer', 'referred', 'created_at', 'completed_at')