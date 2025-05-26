"""
ASGI config for brewery_project project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'brewery_project.settings')

application = get_asgi_application()