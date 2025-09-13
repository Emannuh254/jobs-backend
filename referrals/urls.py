from django.urls import path
from . import views

urlpatterns = [
    path('my-referrals/', views.UserReferralsView.as_view(), name='user-referrals'),
    path('stats/', views.ReferralStatsView.as_view(), name='referral-stats'),
]