from django.contrib import admin
from .models import Job

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'location', 'job_type', 'experience_level', 'posted_by', 'is_active', 'created_at')
    list_filter = ('is_active', 'job_type', 'experience_level', 'created_at')
    search_fields = ('title', 'company', 'description')
    date_hierarchy = 'created_at'
    
    fieldsets = (
        (None, {'fields': ('title', 'description', 'company')}),
        ('Details', {'fields': ('location', 'salary_min', 'salary_max', 'currency')}),
        ('Job Info', {'fields': ('job_type', 'experience_level', 'expires_at')}),
        ('Status', {'fields': ('is_active', 'posted_by')}),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # Only set posted_by on creation
            obj.posted_by = request.user
        super().save_model(request, obj, form, change)