from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import Referral
from .serializers import ReferralSerializer

class UserReferralsView(generics.ListAPIView):
    serializer_class = ReferralSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Referral.objects.filter(referrer=self.request.user)

class ReferralStatsView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        user = request.user
        referrals_count = Referral.objects.filter(referrer=user).count()
        pending_count = Referral.objects.filter(referrer=user, status='pending').count()
        completed_count = Referral.objects.filter(referrer=user, status='completed').count()
        total_points = user.points
        
        return Response({
            'referral_code': user.referral_code,
            'total_referrals': referrals_count,
            'pending_referrals': pending_count,
            'completed_referrals': completed_count,
            'total_points': total_points
        })