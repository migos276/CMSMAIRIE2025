"""
WSGI config for E-CMS project.
"""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'e_cms.settings')
application = get_wsgi_application()
