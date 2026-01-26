import os
from django.core.wsgi import get_wsgi_application

# Settings file ka path set kar rahe hain
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pokky_main.settings')

# Ye wo variable hai jo missing tha
application = get_wsgi_application()