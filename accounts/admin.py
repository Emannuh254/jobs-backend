from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.admin.sites import NotRegistered

# Unregister User only if it's already registered
try:
    admin.site.unregister(User)
except NotRegistered:
    pass

# Now register it again with custom settings if you want
@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "is_staff", "is_active", "date_joined")
    search_fields = ("username", "email")
    list_filter = ("is_staff", "is_active", "is_superuser")
