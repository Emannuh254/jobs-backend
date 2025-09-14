import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jobportal.settings')

application = get_wsgi_application()

# This is for Render to use the PORT environment variable
if __name__ == "__main__":
    from django.core.management import execute_from_command_line
    execute_from_command_line(['manage.py', 'runserver', f'0.0.0.0:{os.environ.get("PORT", 8000)}'])