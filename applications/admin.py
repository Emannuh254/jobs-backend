from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Application

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('job', 'applicant', 'status', 'applied_at')
    list_filter = ('status', 'applied_at')
    search_fields = ('job__title', 'applicant__username')
    date_hierarchy = 'applied_at'
    
    fieldsets = (
        (None, {'fields': ('job', 'applicant')}),
        ('Status', {'fields': ('status', 'notes')}),
    )