from django.contrib import admin
from .models import Referral

@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    list_display = ('referrer', 'referred', 'points_earned', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('referrer__username', 'referred__username')
    date_hierarchy = 'created_at'
    
    actions = ['mark_completed', 'mark_expired']
    
    def mark_completed(self, request, queryset):
        from django.utils import timezone
        updated = queryset.update(status='completed', completed_at=timezone.now())
        self.message_user(request, f'{updated} referrals marked as completed.')
    mark_completed.short_description = "Mark selected referrals as completed"
    
    def mark_expired(self, request, queryset):
        updated = queryset.update(status='expired')
        self.message_user(request, f'{updated} referrals marked as expired.')
    mark_expired.short_description = "Mark selected referrals as expired"